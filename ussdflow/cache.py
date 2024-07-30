import json
import os
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Literal, Optional

import redis
from sqlalchemy import Column, MetaData, String, Table
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError

from ussdflow.models import USSDSession


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
    def __init__(self, sessionmaker, cache_table: str = "cache"):
        """
        Initialize the PostgresCache.

        :param sessionmaker: SQLAlchemy sessionmaker instance.
        :param cache_table: Name of the cache table.
        """
        self.Session = sessionmaker
        self.metadata = MetaData()

        self.cache_table = Table(
            cache_table,
            self.metadata,
            Column("key", String, primary_key=True),
            Column("value", String, nullable=False),
        )

        # Assuming the engine is associated with the sessionmaker
        self.metadata.create_all(self.Session.kw["bind"])

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def set(self, key: str, value):
        """
        Set a value in the cache.

        :param key: The key under which the value is stored.
        :param value: The value to store.
        """
        stmt = insert(self.cache_table).values(key=key, value=value.model_dump_json())
        stmt = stmt.on_conflict_do_update(
            index_elements=["key"], set_={"value": value.model_dump_json()}
        )

        with self.session_scope() as session:
            session.execute(stmt)

    def get(self, key: str) -> str:
        """
        Get a value from the cache.

        :param key: The key to look up.
        :return: The cached value or None if the key does not exist.
        """
        with self.session_scope() as session:
            result = session.execute(
                self.cache_table.select().where(self.cache_table.c.key == key)
            ).fetchone()
            return result["value"] if result else None

    def delete(self, key: str):
        """
        Delete a value from the cache.

        :param key: The key to delete.
        """
        with self.session_scope() as session:
            session.execute(
                self.cache_table.delete().where(self.cache_table.c.key == key)
            )


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
    """
    CacheManager is a class that provides a unified interface
    for different types of caches.
    Supported cache types are Redis, PostgreSQL, file-based caches,
    and custom cache objects.

    :param cache_type: Specifies the type of cache to use. Must be one of
    'redis', 'postgres', 'file', or 'custom'.
    :param custom_cache: An optional custom cache object. If provided,
    it overrides the cache_type parameter.
    :param kwargs: Additional keyword arguments specific to the chosen cache type.

    Keyword Arguments (kwargs):
        - For RedisCache:
            - client: Redis client instance.
            - config: Configuration for Redis client.
        - For PostgresCache:
            - sessionmaker: SQLAlchemy sessionmaker instance.
            - cache_table: Name of the cache table.
        - For FileCache:
            - file_path: Path to the file used for storing cache data.

    Raises:
        ValueError: If an unsupported cache type is provided.
    """

    def __init__(
        self,
        cache_type: Literal["redis", "postgres", "file", "custom"],
        custom_cache: Optional[Cache] = None,
        **kwargs,
    ):
        """
        Initialize the CacheManager.

        :param cache_type: Specifies the type of cache to use
        ('redis', 'postgres', 'file', or 'custom').
        :param custom_cache: An optional custom cache object. If provided,
        it overrides the cache_type parameter.
        :param kwargs: Additional keyword arguments specific to the chosen cache type.
        """
        if custom_cache is not None:
            self.cache = custom_cache
        else:
            if cache_type == "redis":
                self.cache = RedisCache(**kwargs)
            elif cache_type == "postgres":
                self.cache = PostgresCache(**kwargs)
            elif cache_type == "file":
                self.cache = FileCache(**kwargs)
            else:
                raise ValueError(f"Unsupported cache type: {cache_type}")

    def set(self, key: str, value: USSDSession) -> USSDSession:
        """
        Set a value in the cache.

        :param key: The key under which the value is stored.
        :param value: The USSDSession object to store.
        :return: The stored USSDSession object.
        """
        self.cache.set(key, value)
        return value

    def get(self, key: str) -> USSDSession | None:
        """
        Get a value from the cache.

        :param key: The key to look up.
        :return: The cached USSDSession object, or None if the key does not exist.
        """
        return self.cache.get(key)

    def delete(self, key: str):
        """
        Delete a value from the cache.

        :param key: The key to delete.
        """
        self.cache.delete(key)
