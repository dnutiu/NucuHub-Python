import pytest

from nucuhub.config import ApplicationConfig
from nucuhub.infrastructure.redis import RedisService


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
