from domain.config import ApplicationConfig
from domain.logging import get_logger

logger = get_logger("RedisService")


class RedisService:
    __singleton = None
    __connection_pool = None

    def __init__(self, redis_url):
        """
            Don't call this method directly instead use instance.
        """
        pass

    @classmethod
    def instance(cls):
        if cls.__singleton is None:
            redis_url = ApplicationConfig.REDIS_URL
            logger.info(f"RedisSingleton: Setting Connection String={redis_url}")
            cls.__singleton = cls(redis_url=redis_url)
        return cls.__singleton

    @classmethod
    def set_singleton(cls, singleton):
        cls.__singleton = singleton

    def get_redis(self):
        pass
