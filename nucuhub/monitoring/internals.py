import queue
import time

from nucuhub.domain.utils import is_string
from nucuhub.logging import get_logger
from nucuhub.monitoring import infrastructure

__all__ = ["ProducerException", "Producer"]


class ProducerException(Exception):
    pass


class Producer:
    """
        Producer that retrieves messages from the topics of interests.
    """

    def __init__(self, queue_: queue.Queue):
        self.message_broker = infrastructure.Messaging()
        self._logger = get_logger("MonitoringProducer")
        self._queue = queue_
        self.loop_should_run = None
        self.sleep_time = 1
        self.pending_messages = []

    def _process_message(self):
        message = self.message_broker.get_message()
        self._logger.debug(f"Polling messages. Got: {message}")

        try:
            if self.pending_messages:
                self._queue.put(
                    self.pending_messages.pop(0), block=True, timeout=self.sleep_time
                )
            if message:
                self._queue.put(message, block=True, timeout=self.sleep_time)
        except queue.Full:
            self._logger.debug("Queue is full!")
            self.pending_messages.append(message)

    def _loop_forever(self):
        while self.loop_should_run:
            self._process_message()
            self._sleep()

    def loop_forever(self):
        """
            Blocking operation that will make the producer work.
        :return:
        """
        self._logger.info("Looping forever!")
        self.loop_should_run = True
        if self._queue is None:
            self._logger.fatal("Queue can't be none!")
        self.message_broker.subscribe_to_all()
        self._loop_forever()
        self.message_broker.unsubscribe_from_all()

    def _sleep(self):
        time.sleep(self.sleep_time)

    def set_topics(self, topics):
        """
            Sets the topics the producer should subscribe to.
        :param topics: A list of topics or a single string.
        """
        if not topics:
            raise ProducerException("Topics can't be empty!")
        if isinstance(topics, str):
            if not topics:
                raise ProducerException("Topics can't be empty!")
            self.message_broker.TOPICS_OF_INTEREST = [topics]
        else:
            topics = list(filter(is_string, topics))
            if len(topics) == 0:
                raise ProducerException("Topics can't be empty!")
            self.message_broker.TOPICS_OF_INTEREST = topics

    def get_topics(self):
        """
            Gets the topic of interest for the producer.
        :return: The topics as a list.
        """
        return self.message_broker.TOPICS_OF_INTEREST

    def shutdown(self):
        """
            Stops the producer from looping.
        """
        self._logger.info("Shutting down producer.")
        self.loop_should_run = False
