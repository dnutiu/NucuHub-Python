import abc
import queue
import time
import typing

from nucuhub.domain.utils import is_string
from nucuhub.logging import get_logger, get_null_logger
from nucuhub.monitoring import infrastructure

__all__ = [
    "ProducerException",
    "Producer",
    "ConsumerStage",
    "Consumer",
    "ConsumerException",
]


class WorkerBase(abc.ABC):
    def __init__(self, queue_: queue.Queue):
        self._logger = get_null_logger()
        self._queue = queue_
        self._loop_should_run = None
        self.sleep_time = 1

    def init_logger(self, name):
        """
            Initializes basic logging.
        :param name: The logger's name.
        """
        self._logger = get_logger(name)

    def loop_forever(self):
        """
            Blocking operation that will make the producer work.
        :return:
        """
        self._logger.info("Looping forever!")
        self._loop_should_run = True
        if self._queue is None:
            self._logger.fatal("Queue can't be none!")

    def _sleep(self):
        time.sleep(self.sleep_time)

    def shutdown(self):
        """
            Stops the worker from looping.
        """
        self._loop_should_run = False

    def _loop_forever(self):
        while self._loop_should_run:
            self._process_message()
            self._sleep()

    def _process_message(self):
        """
            Processes the message from the queue.
        :return: Nothing.
        """
        raise NotImplementedError()


class ProducerException(Exception):
    pass


class Producer(WorkerBase):
    """
        Producer that retrieves messages from the topics of interests.
    """

    def __init__(self, queue_: queue.Queue):
        super().__init__(queue_)
        self.init_logger("MonitoringProducer")
        self.message_broker = infrastructure.Messaging()
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

    def loop_forever(self):
        """
            Blocking operation that will make the producer work.
        :return:
        """
        super(Producer, self).loop_forever()
        self.message_broker.subscribe_to_all()
        self._loop_forever()
        self.message_broker.unsubscribe_from_all()

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
        super(Producer, self).shutdown()
        self._logger.info("Shutting down producer.")


class ConsumerStage:
    """
        Class that is used in the Consumer for message processing.
    """

    name: str = NotImplemented

    def process(self, message):
        """
            The process function processes the message.
        :param message: The message that will be processed.
        :return: True if the flow to the next stage should stop, False otherwise.
        """
        raise NotImplementedError()

    def __str__(self):
        return self.name


class ConsumerException(Exception):
    pass


class Consumer(WorkerBase):
    """
        Consumes messages from the queue and takes each message through a number of
        user-defined stages. See ConsumerStage.

        If a stage returns False the processing for that message stops.

        Example stages:
            filter -> log -> upload to cloud -> execute code
    """

    def __init__(self, queue_: queue.Queue):
        super().__init__(queue_)
        self.init_logger("MonitoringConsumer")
        self._pipeline_stages = []

    def _process_message(self):
        try:
            message = self._queue.get(block=True, timeout=self.sleep_time)
            self._logger.debug(f"Polling messages. Got: {message}")
            if message:
                for stage in self._pipeline_stages:
                    to_continue = stage.process(message)
                    if not to_continue:
                        break
        except queue.Empty:
            self._logger.debug("Queue empty!")

    def add_stage(self, new_stage: typing.ClassVar[ConsumerStage]):
        """
            Adds a stage to the pipeline stages, each stage must have a unique name.
        :param new_stage: The ConsumerStage instance.
        :raises: ConsumerException if a stage with the same name already exists.
        """
        for stage in self._pipeline_stages:
            if stage.name == new_stage.name:
                raise ConsumerException(
                    "ConsumerStages must have a unique name! {name} is already present in the pipeline."
                )
        self._pipeline_stages.append(new_stage)

    def remove_stage(self, name):
        """
            Removes a stage from the pipeline stages by name.
        :return: True if the stage was removed, false otherwise.
        """
        for stage in self._pipeline_stages:
            if stage.name == name:
                self._pipeline_stages.remove(stage)
                return True
        return False

    def loop_forever(self):
        """
            Blocking operation that will make the consumer work.
        :return:
        """
        super(Consumer, self).loop_forever()
        self._loop_forever()

    def shutdown(self):
        """
            Stops the producer from looping.
        """
        self._logger.info("Shutting down producer.")
        super(Consumer, self).shutdown()
