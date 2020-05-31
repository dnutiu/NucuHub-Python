import redis

from nucuhub.domain.config import ApplicationConfig
from nucuhub.domain.logging import get_logger

logger = get_logger("RedisService")


class RedisService:
    __singleton = None
    __client = None

    def __init__(self):
        """
            Don't call this method directly instead use instance.
        """
        pass

    @classmethod
    def instance(cls):
        if cls.__singleton is None:
            cls.redis_url = ApplicationConfig.REDIS_URL
            logger.info(f"RedisSingleton: Setting Connection String={cls.redis_url}")
            cls.__singleton = cls()
            cls.__client = redis.Redis(cls.redis_url)
        return cls.__singleton

    @classmethod
    def set_singleton(cls, singleton):
        cls.__singleton = singleton

    def get_redis(self):
        return self.__client
