import random
import typing

from nucuhub.domain.sensors import SensorMeasurement
from nucuhub.domain.sensors.config import SensorConfig
from nucuhub.sensors.internals import SensorModule


class DummySensor(SensorModule):
    def _configure(self):
        return SensorConfig(
            id="tid",
            name="tests-sesnro",
            description="the tests description",
            enabled=False,
        )

    def _get_data(self) -> typing.List[SensorMeasurement]:
        return [
            SensorMeasurement(
                sensor_id="dummy_sensor",
                name="tests",
                description="tests",
                value=random.choice([1, 0]),
                timestamp=0,
            )
        ]


class ExactDummySensor(DummySensor):
    def _configure(self):
        return SensorConfig(
            id="tid",
            name="tests-sesnro",
            description="the tests description",
            enabled=True,
        )

    def _get_data(self) -> typing.List[SensorMeasurement]:
        return [
            SensorMeasurement(
                sensor_id="dummy_sensor",
                name="tests",
                description="tests",
                value=2.22,
                timestamp=0,
            )
        ]
