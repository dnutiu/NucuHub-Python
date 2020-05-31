import pytest

from nucuhub.domain.config import ApplicationConfig
from nucuhub.infrastructure.redis import RedisService


@pytest.fixture
def redis_fixture():
    ApplicationConfig.REDIS_URL = "localhost"
    RedisService.set_singleton(None)
    redis = RedisService.instance()
    return redis
