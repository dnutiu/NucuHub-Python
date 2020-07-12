import pytest


def test_messaging_subscribe_to_all(messaging):
    messaging.TOPICS_OF_INTEREST = ["test_topic1", "test_topic2"]
    messaging.subscribe_to_all()
    assert messaging._pubsub.subscribed is True
    assert set(map(lambda i: i.decode(), messaging._pubsub.channels)) == set(
        messaging.TOPICS_OF_INTEREST
    )


def test_messaging_unsubscribe_from_all(messaging):
    messaging.TOPICS_OF_INTEREST = ["test_topic1", "test_topic2"]
    messaging.subscribe_to_all()
    messaging.unsubscribe_from_all()
    assert set(
        map(lambda i: i.decode(), messaging._pubsub.pending_unsubscribe_channels)
    ) == set(messaging.TOPICS_OF_INTEREST)


def test_messaging_get_data(messaging):
    messaging.TOPICS_OF_INTEREST = ["testing"]
    messaging.subscribe_to_all()
    messaging.get_message()  # ignore subscribe messaging
    redis = messaging.client.get_redis()
    redis.publish("testing", "test-data")
    message = messaging.get_message()
    assert messaging.decode_message_data(message) == "test-data"


@pytest.mark.parametrize(
    "message_data, expected",
    [
        pytest.param(b"simple-string", "simple-string"),
        pytest.param(1996, 1996),
        pytest.param(1996.1, 1996.1),
        pytest.param(b'{"ok":true}', {"ok": True}),
    ],
)
def test_messaging_decode_data(messaging, message_data, expected):
    assert messaging.decode_message_data({"data": message_data}) == expected
