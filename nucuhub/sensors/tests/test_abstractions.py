from unittest.mock import MagicMock

import pytest

from nucuhub.domain.sensors import SensorException
from nucuhub.domain.sensors.config import SensorState
from nucuhub.sensors.tests.mocks import DummySensor


def test_sensor_module_read(redis_fixture):
    # normal read
    sensor = DummySensor()
    sensor.enable()
    assert sensor.get_data() is not None
    # can't read when disabled
    sensor.disable()
    with pytest.raises(SensorException):
        sensor.get_data()


def test_sensor_module_initialize(redis_fixture):
    # Copy the class in order to avoid un-setting the mocks.
    dummy_sensor = type(
        "DummySensorCopy", DummySensor.__bases__, dict(DummySensor.__dict__)
    )
    c_mock = dummy_sensor._configure = MagicMock()
    lc_mock = dummy_sensor._load_config = MagicMock()
    dummy_sensor()
    assert c_mock.called is True
    assert lc_mock.called is True


@pytest.mark.parametrize(
    "getter, expected",
    [
        pytest.param("name", "test-sesnro"),
        pytest.param("description", "the test description"),
        pytest.param("is_enabled", False),
    ],
)
def test_sensor_module_getters(redis_fixture, getter, expected):
    sensor = DummySensor()
    assert getattr(sensor, getter) == expected


@pytest.mark.parametrize(
    "action, expected", [pytest.param("enable", True), pytest.param("disable", False)]
)
def test_sensor_module_enabling(redis_fixture, action, expected):
    sensor = DummySensor()
    # Call the method
    getattr(sensor, action)()
    # Compare the values
    assert sensor.is_enabled == expected


@pytest.mark.parametrize(
    "action, expected",
    [
        pytest.param("set_state", SensorState.OK, id="state_ok"),
        pytest.param("set_state", SensorState.ERROR, id="state_error"),
    ],
)
def test_sensor_module_set_state(redis_fixture, action, expected):
    sensor = DummySensor()
    # Call the method
    getattr(sensor, action)(expected)
    # Compare the values
    assert sensor.state == expected.value
