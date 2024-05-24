import json
from unittest.mock import MagicMock

import pytest
from sqlalchemy.dialects.postgresql import insert
from ussd_lib.cache import CacheManager, PostgresCache
from ussd_lib.models import USSDSession


@pytest.fixture
def mock_sessionmaker(mocker):
    # Create a mock sessionmaker
    mock_session = mocker.MagicMock()
    mock_sessionmaker = mocker.Mock(return_value=mock_session)
    mock_sessionmaker.kw = {"bind": MagicMock()}
    return mock_sessionmaker


@pytest.fixture
def cache(mock_sessionmaker):
    # Create an instance of PostgresCache with the mock sessionmaker
    return PostgresCache(mock_sessionmaker)


def test_postgres_get_cache(mock_sessionmaker, cache):
    # Arrange
    key = "test_key"
    expected_value = "test_value"
    mock_result = {"value": expected_value}
    mock_sessionmaker().execute.return_value.fetchone.return_value = mock_result

    # Act
    result = cache.get(key)

    # Assert
    assert result == expected_value
    mock_sessionmaker().execute.assert_called()
    stmt = mock_sessionmaker().execute.call_args[0][0]
    assert stmt is not None  # Verify that the statement is constructed


def test_postgres_get_cache_key_not_found(mock_sessionmaker, cache):
    # Arrange
    key = "test_key"
    mock_sessionmaker().execute.return_value.fetchone.return_value = None

    # Act
    result = cache.get(key)

    # Assert
    assert result is None
    mock_sessionmaker().execute.assert_called()
    stmt = mock_sessionmaker().execute.call_args[0][0]
    assert stmt is not None  # Verify that the statement is constructed


def test_postgres_delete_cache(mock_sessionmaker, cache):
    # Arrange
    key = "test_key"

    # Act
    cache.delete(key)

    # Assert
    mock_sessionmaker().execute.assert_called()
    stmt = mock_sessionmaker().execute.call_args[0][0]
    assert stmt is not None  # Verify that the statement is constructed


def test_postgres_set_cache(mock_sessionmaker, cache, mocker):
    # Arrange
    key = "test_key"
    value = mocker.MagicMock()
    value.model_dump_json.return_value = '{"data": "test_value"}'

    # Act
    cache.set(key, value)

    # Assert
    mock_sessionmaker().execute.assert_called()
    stmt = mock_sessionmaker().execute.call_args[0][0]
    # assert isinstance(stmt, insert)  # Verify that the statement is an insert object
    assert stmt.table.name == "cache"  # Verify that the table name is correct


def test_redis_cache_get(mock_redis_client):
    client = mock_redis_client.return_value
    cache_manager = CacheManager(cache_type="redis", client=client)
    session = USSDSession(
        id="1",
        session_id="session123",
        service_code="*123#",
        phone_number="123456789",
        text="some text",
        previous_menu_level="1",
        current_menu_level="2",
    )
    client.get.return_value = json.dumps(session.model_dump())
    result = cache_manager.get("session_key")
    assert result == session.model_dump()


def test_redis_cache_delete(mock_redis_client):
    client = mock_redis_client.return_value
    cache_manager = CacheManager(cache_type="redis", client=client)
    cache_manager.delete("session_key")
    client.delete.assert_called_with("session_key")
