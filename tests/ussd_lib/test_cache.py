import json
import pytest

from unittest.mock import MagicMock, create_autospec
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from ussd_lib.cache import CacheManager
from ussd_lib.models import USSDSession


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
