import json

from nucuhub.infrastructure.redis import RedisService
from nucuhub.logging import get_logger


class RedisBackend:
    client: RedisService = None

    def __init__(self):
        self.client = RedisService.instance()


class Messaging(RedisBackend):
    TOPICS_OF_INTEREST = ["sensors"]
    logger = None

    def __init__(self):
        super().__init__()
        self._pubsub = self.client.get_redis().pubsub()
        self.logger = get_logger("MonitoringMessaging")

    def subscribe_to_all(self):
        """
            Subscribe to the topics of interest
        """
        for topic in self.TOPICS_OF_INTEREST:
            self.logger.info(f"Subscribe to: {topic}.")
            self._pubsub.subscribe(topic)

    def unsubscribe_from_all(self):
        """
            Unsubscribe from the topics of interest
        """
        self._pubsub.unsubscribe()

    def get_message(self, timeout=1):
        """
            Retrieves a message.
        :return:  The message data as a python dict.
        """
        message = self._pubsub.get_message(
            ignore_subscribe_messages=True, timeout=timeout
        )
        return message

    @staticmethod
    def decode_message_data(message):
        if not message:
            return None

        return_value = message.get("data")

        if isinstance(return_value, bytes):
            return_value = return_value.decode()

        try:
            return_value = json.loads(return_value)
        except (TypeError, AttributeError, json.decoder.JSONDecodeError):
            pass
        return return_value
