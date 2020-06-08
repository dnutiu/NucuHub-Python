import enum
from dataclasses import dataclass


class SensorState(enum.Enum):
    OK = "OK"
    ERROR = "ERROR"


@dataclass
class SensorConfig:
    id: str
    name: str
    description: str
    enabled: bool
    state: str

    def __init__(self, id, name, description, enabled, state=None):
        self.id = id
        self.name = name
        self.description = description
        self.enabled = enabled
        self.state = SensorState.OK.value
