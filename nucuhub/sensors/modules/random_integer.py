import random
import typing

from nucuhub import utils
from nucuhub.sensors.types import SensorConfig, SensorMeasurement, SensorModule


class RandomInteger(SensorModule):
    sensor_id = "random_integer"

    def _configure(self) -> SensorConfig:
        return SensorConfig(
            id=self.sensor_id,
            name="Random Integer",
            description="Outputs a random integer value",
            enabled=False,
        )

    def _get_data(self) -> typing.List[SensorMeasurement]:
        return_value = []
        timestamp = utils.get_now_timestamp()
        return_value.append(
            SensorMeasurement(
                sensor_id=self.sensor_id,
                name="random_int_1",
                description="A random integer between 0 and 15.",
                value=random.randint(0, 15),
                timestamp=timestamp,
            )
        )
        return_value.append(
            SensorMeasurement(
                sensor_id=self.sensor_id,
                name="random_int_2",
                description="A random integer between 100 and 200",
                value=random.randint(100, 200),
                timestamp=timestamp,
            )
        )
        return return_value
