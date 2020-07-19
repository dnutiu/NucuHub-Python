from dataclasses import dataclass

from nucuhub.sensors.types import SensorState


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
