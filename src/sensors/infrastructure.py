from src.infrastructure.redis import RedisService


class RedisBackend:
    client: RedisService = None

    def __init__(self):
        self.client = RedisService.instance()


class Messaging(RedisBackend):
    def publish(self, data):
        pass  # TODO push to redis


class Database(RedisBackend):
    def save_config(self, name, data):
        pass  # TODO save to redis

    def load_config(self, name):
        pass  # TODO load from redis
