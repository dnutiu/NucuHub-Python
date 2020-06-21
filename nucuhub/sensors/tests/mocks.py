import random
import typing

from nucuhub.domain.sensors import SensorMeasurement, SensorModule
from nucuhub.domain.sensors.config import SensorConfig


class DummySensor(SensorModule):
    def _configure(self):
        return SensorConfig(
            id="tid",
            name="test-sesnro",
            description="the test description",
            enabled=False,
        )

    def _get_data(self) -> typing.List[SensorMeasurement]:
        return [
            SensorMeasurement(
                sensor_id="dummy_sensor",
                name="test",
                description="test",
                value=random.choice([1, 0]),
                timestamp=0,
            )
        ]


class ExactDummySensor(DummySensor):
    def _configure(self):
        return SensorConfig(
            id="tid",
            name="test-sesnro",
            description="the test description",
            enabled=True,
        )

    def _get_data(self) -> typing.List[SensorMeasurement]:
        return [
            SensorMeasurement(
                sensor_id="dummy_sensor",
                name="test",
                description="test",
                value=2.22,
                timestamp=0,
            )
        ]
