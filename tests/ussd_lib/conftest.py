import pytest
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="session")
def engine():
    from pytest_postgresql.factories import postgresql_proc

    # Start the PostgreSQL process
    postgresql = postgresql_proc()

    # Create an SQLAlchemy engine
    engine = create_engine(postgresql.url())

    return engine


@pytest.fixture(scope="session")
def tables(engine):
    # Create metadata
    metadata = MetaData()
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.fixture(scope="function")
def dbsession(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def mock_redis_client(mocker):
    return mocker.patch("redis.StrictRedis")
