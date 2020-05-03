import typing

from sensors.abstractions import SensorMeasurement, SensorModule
from sensors.config import SensorConfig


class CpuTemperature(SensorModule):
    file_name = "/sys/class/thermal/thermal_zone2/temp"

    def _configure(self) -> SensorConfig:
        return SensorConfig(
            id="cpu_temperature_sensor",
            name="Cpu Temp",
            description="Outputs the CPU temperature in celsius",
            enabled=False,
        )

    def _get_data(self) -> typing.List[SensorMeasurement]:
        with open(self.file_name) as fd:
            data = fd.readline()
        return [
            SensorMeasurement(
                name="thermal_zone2",
                description="CPU package temperature in celsius",
                value=float(data) / 1000,
            )
        ]
