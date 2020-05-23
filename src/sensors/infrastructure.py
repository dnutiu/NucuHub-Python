import json

from src.infrastructure.redis import RedisService


class RedisBackend:
    client: RedisService = None

    def __init__(self):
        self.client = RedisService.instance()


class Messaging(RedisBackend):
    def publish(self, data):
        redis = self.client.get_redis()
        redis.publish("sensors", json.dumps(data))


class Database(RedisBackend):
    def save_config(self, name, data):
        redis = self.client.get_redis()
        redis.set(name, json.dumps(data))

    def load_config(self, name):
        redis = self.client.get_redis()
        data = redis.get(name)
        return_val = None
        if data:
            return_val = json.loads(data.decode())
        return return_val
