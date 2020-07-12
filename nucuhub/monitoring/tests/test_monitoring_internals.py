from queue import Queue

import pytest

from nucuhub.monitoring import internals
from nucuhub.monitoring.tests import mocks


def create_producer(queue_max_size, topics):
    queue = Queue(queue_max_size)
    producer = internals.Producer(queue)
    producer.set_topics(topics)
    return queue, producer


def create_consumer(queue_max_size):
    queue = Queue(queue_max_size)
    consumer = internals.Consumer(queue)
    return queue, consumer


@pytest.mark.parametrize(
    "topics, expected",
    [
        pytest.param("test_topic", ["test_topic"], id="string-topic"),
        pytest.param(["1", "2"], ["1", "2"], id="topic-multiple"),
        pytest.param(["1", 2], ["1"], id="non-string-ignored"),
    ],
)
def test_producer_get_set_topics(messaging, topics, expected):
    _, worker = create_producer(1, topics)
    assert worker.get_topics() == expected


@pytest.mark.parametrize(
    "topics",
    [
        pytest.param(None, id="string-topic"),
        pytest.param("", id="string-empty-topic"),
        pytest.param([], id="topic-multiple"),
    ],
)
def test_producer_get_set_topics_exception(messaging, topics):
    with pytest.raises(internals.ProducerException):
        create_producer(1, topics)


# noinspection DuplicatedCode
def test_producer_process_message_simple(messaging):
    """
        Ensure that the producer can queue simple messages.
    """
    redis = messaging.client.get_redis()
    queue, producer = create_producer(5, "test_topic")
    producer.message_broker.subscribe_to_all()
    redis.publish("test_topic", "tm1")
    redis.publish("test_topic", "tm2")
    producer._process_message()  # ignore subscribe message
    producer._process_message()  # process tm1
    producer._process_message()  # process tm2

    # Will raise queue.Empty exception if message was not properly processed.
    assert messaging.decode_message_data(queue.get(timeout=0.5)) == "tm1"
    assert messaging.decode_message_data(queue.get(timeout=0.5)) == "tm2"


# noinspection DuplicatedCode
def test_producer_process_message_pending(messaging):
    """
        Ensure that the producer can queue messages when the queue has reached it's maxsize.
    """
    redis = messaging.client.get_redis()
    queue, producer = create_producer(1, "test_topic")
    producer.message_broker.subscribe_to_all()

    redis.publish("test_topic", "tm1")
    redis.publish("test_topic", "tm2")
    producer._process_message()  # ignore subscribe message
    producer._process_message()  # process tm1
    producer._process_message()  # queue is full
    assert messaging.decode_message_data(queue.get(timeout=0.5)) == "tm1"
    producer._process_message()  # process pending tm2
    assert messaging.decode_message_data(queue.get(timeout=0.5)) == "tm2"


def test_producer_shutdown(messaging):
    _, producer = create_producer(1, "topics")
    producer.shutdown()
    assert producer._loop_should_run is False


def test_consumer_shutdown(messaging):
    _, consumer = create_consumer(1)
    consumer.shutdown()
    assert consumer._loop_should_run is False


def test_consumer_add_stage():
    _, consumer = create_consumer(1)
    test_stage = internals.ConsumerStage()
    # If nothing happens add is successful.
    consumer.add_stage(test_stage)
    with pytest.raises(internals.ConsumerException):
        consumer.add_stage(test_stage)


def test_consumer_remove_stage():
    _, consumer = create_consumer(1)
    test_stage = internals.ConsumerStage()
    test_stage.name = "test-stage"
    # If nothing happens add is successful.
    consumer.add_stage(test_stage)
    assert consumer.remove_stage("test-stage") is True
    assert consumer.remove_stage("test-stage") is False


def test_consumer_process():
    """
        Ensure that the consumer can move the message in two distinct stages.
    :return:
    """
    q, consumer = create_consumer(1)
    test_stage = mocks.MockConsumerStage()
    test_stage2 = mocks.MockConsumerStageException()
    consumer.add_stage(test_stage)
    consumer.add_stage(test_stage2)
    q.put({"test": True})
    with pytest.raises(ValueError):
        consumer._process_message()
    assert test_stage.processed is True
    # The queue is empty, the exception should be handled.
    consumer._process_message()
