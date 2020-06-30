import enum
import typing
from dataclasses import dataclass


@dataclass
class SensorMeasurement:
    sensor_id: str
    name: str
    description: str
    timestamp: int
    value: typing.Union[int, float, str]


class SensorState(enum.Enum):
    OK = "OK"
    ERROR = "ERROR"
