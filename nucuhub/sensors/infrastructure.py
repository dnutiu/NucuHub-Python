import json

from nucuhub.infrastructure.redis import RedisService
from nucuhub.logging import get_logger

logger = get_logger("sensors.infrastructure")


class RedisBackend:
    client: RedisService = None

    def __init__(self):
        self.client = RedisService.instance()


class Messaging(RedisBackend):
    def __init__(self):
        super().__init__()
        self._pubsub = self.client.get_redis().pubsub()
        self._pubsub.subscribe("sensors_cmd")
        self.logger = get_logger("SensorsMessaging")

    def publish(self, data):
        """
            Publishes data to the sensors topic on Redis.
        """
        redis = self.client.get_redis()
        logger.debug(data)
        redis.publish("sensors", json.dumps(data))

    def get_command(self):
        """
            Retrieves a sensor command.
        :return:  The message data as a python dict.
        """
        return_value = None
        try:
            message = self._pubsub.get_message(
                ignore_subscribe_messages=True, timeout=1
            )
            if message:
                return_value = json.loads(message.get("data"))
        except (TypeError, AttributeError) as e:
            self.logger.debug(f"error in get_message: {e}")
            return_value = None
        return return_value


class Database(RedisBackend):
    def save_config(self, name, data):
        """
            Saves sensor config in the database
        :param name: The key name, usually sensor id.
        :param data: The configuration data.
        """
        redis = self.client.get_redis()
        redis.set(name, json.dumps(data))

    def load_config(self, name):
        """
            Loads the config from the database
        :param name: The key name, usually sensor id.
        :return: Returns the configuration data as a python dict if it exists, otherwise none.
        """
        redis = self.client.get_redis()
        data = redis.get(name)
        return_val = None
        if data:
            return_val = json.loads(data.decode())
        return return_val
