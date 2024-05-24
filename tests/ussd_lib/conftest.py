import pytest


@pytest.fixture
def mock_redis_client(mocker):
    return mocker.patch("redis.StrictRedis")
