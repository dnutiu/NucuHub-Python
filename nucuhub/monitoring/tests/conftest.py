import pytest

from nucuhub.config import ApplicationConfig
from nucuhub.infrastructure.redis import RedisService
from nucuhub.monitoring.infrastructure import Messaging


@pytest.fixture
def redis_fixture():
    redis = None
    try:
        ApplicationConfig.REDIS_URL = "localhost"
        RedisService.set_singleton(None)
        redis = RedisService.instance()
        yield redis
    finally:
        if redis is not None:
            redis.get_redis().flushall()


@pytest.fixture()
def messaging(redis_fixture):
    client = Messaging()
    yield client
