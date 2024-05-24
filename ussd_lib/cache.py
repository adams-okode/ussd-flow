import redis
import os
import json

from typing import Literal
from sqlalchemy import create_engine, Column, String, Table, MetaData, insert
from sqlalchemy.orm import sessionmaker
from abc import ABC, abstractmethod

from ussd_lib.models import USSDSession


class Cache(ABC):
    @abstractmethod
    def set(self, key, value):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def delete(self, key):
        pass


class RedisCache(Cache):
    def __init__(self, client=None, config=None):
        config = config or {"host": "localhost", "port": 6379, "db": 0}
        self.client = client or redis.StrictRedis(
            host=config["host"], port=config["port"], db=config["db"]
        )

    def set(self, key, value):
        self.client.set(key, json.dumps(value))

    def get(self, key):
        value = self.client.get(key)
        return json.loads(value) if value else None

    def delete(self, key):
        self.client.delete(key)


class PostgresCache(Cache):
    def __init__(self, dsn=None, engine=None, cache_table="cache"):
        self.engine = create_engine(dsn) if dsn is not None else engine
        self.metadata = MetaData()

        self.cache_table = Table(
            cache_table,
            self.metadata,
            Column("key", String, primary_key=True),
            Column("value", String, nullable=False),
        )

        self.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def set(self, key, value: USSDSession):
        session = self.Session()

        stmt = insert(self.cache_table).values(key=key, value=value.model_dump_json())
        # stmt = stmt.on_conflict_do_update(
        #     index_elements=["key"],
        #     set_=dict(value=value.model_dump_json()),
        # )

        with session.begin():
            session.execute(stmt)
        session.close()

    def get(self, key):
        session = self.Session()
        result = session.execute(
            self.cache_table.select().where(self.cache_table.c.key == key)
        ).fetchone()
        session.close()
        return result["value"] if result else None

    def delete(self, key):
        session = self.Session()
        with session.begin():
            session.execute(
                self.cache_table.delete().where(self.cache_table.c.key == key)
            )
        session.close()


class FileCache(Cache):
    def __init__(self, file_path="cache.json"):
        self.file_path = file_path
        # Ensure the file exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({}, f)

    def _read_cache(self):
        with open(self.file_path, "r") as f:
            return json.load(f)

    def _write_cache(self, cache):
        with open(self.file_path, "w") as f:
            json.dump(cache, f)

    def set(self, key, value: USSDSession):
        cache = self._read_cache()
        cache[key] = value.model_dump()
        self._write_cache(cache)

    def get(self, key):
        cache = self._read_cache()
        try:
            if cache[key] is not None:
                return USSDSession(**cache.get(key))
            return None
        except KeyError:
            return None

    def delete(self, key):
        cache = self._read_cache()
        if key in cache:
            del cache[key]
            self._write_cache(cache)


class CacheManager:
    def __init__(self, cache_type: Literal["redis", "postgres", "file"], **kwargs):
        if cache_type == "redis":
            self.cache = RedisCache(**kwargs)
        elif cache_type == "postgres":
            self.cache = PostgresCache(**kwargs)
        elif cache_type == "file":
            self.cache = FileCache(**kwargs)
        else:
            raise ValueError(f"Unsupported cache type: {cache_type}")

    def set(self, key, value: USSDSession) -> USSDSession:
        self.cache.set(key, value)
        return value

    def get(self, key) -> USSDSession | None:
        return self.cache.get(key)

    def delete(self, key):
        self.cache.delete(key)
