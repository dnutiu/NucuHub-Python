from dataclasses import dataclass


@dataclass
class SensorConfig:
    id: str
    name: str
    description: str
    enabled: bool
