import typing

import bme680
from nucuhub.domain import utils
from nucuhub.sensors.config import SensorConfig
from nucuhub.sensors.internals import SensorModule
from nucuhub.sensors.types import SensorMeasurement, SensorState


class Bme680(SensorModule):
    sensor_id = "bme680"
    _sensor = None

    def _initialize(self):
        super(Bme680, self)._initialize()
        try:
            try:
                self._sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
            except IOError:
                self._sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

            self._sensor.set_humidity_oversample(bme680.OS_2X)
            self._sensor.set_pressure_oversample(bme680.OS_4X)
            self._sensor.set_temperature_oversample(bme680.OS_8X)
            self._sensor.set_filter(bme680.FILTER_SIZE_3)
            self._sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

            self._sensor.set_gas_heater_temperature(320)
            self._sensor.set_gas_heater_duration(150)
            self._sensor.select_gas_heater_profile(0)
        except (FileNotFoundError, PermissionError):
            self._logger.error("Bme680 initialization failed!")
            self.set_state(SensorState.ERROR)
            self.disable()

    def _configure(self) -> SensorConfig:
        return SensorConfig(
            id=self.sensor_id,
            name="Cpu Temp",
            description="Outputs the CPU temperature in celsius",
            enabled=True,
        )

    def _get_data(self) -> typing.List[SensorMeasurement]:
        return_value = []
        if self.state == SensorState.ERROR:
            return return_value

        read_ok = self._sensor.get_sensor_data()
        if read_ok:
            timestamp = utils.get_now_timestamp()
            return_value.append(
                SensorMeasurement(
                    sensor_id=self.sensor_id,
                    name="temperature",
                    description="bme680 temperature, celsius",
                    value=self._sensor.data.temperature,
                    timestamp=timestamp,
                )
            )
            return_value.append(
                SensorMeasurement(
                    sensor_id=self.sensor_id,
                    name="pressure",
                    description="bme680 pressure. hPa",
                    value=self._sensor.data.pressure,
                    timestamp=timestamp,
                )
            )
            return_value.append(
                SensorMeasurement(
                    sensor_id=self.sensor_id,
                    name="humidity",
                    description="bme680 humidity, %RH",
                    value=self._sensor.data.humidity,
                    timestamp=timestamp,
                )
            )
            return_value.append(
                SensorMeasurement(
                    sensor_id=self.sensor_id,
                    name="gas_resistance",
                    description="bme680 gas resistance, Ohms",
                    value=self._sensor.data.gas_resistance,
                    timestamp=timestamp,
                )
            )
            # If heat_stable is false then gas_resistance is not ok
            return_value.append(
                SensorMeasurement(
                    sensor_id=self.sensor_id,
                    name="heat_stable",
                    description="bme680 heat_stable, boolean",
                    value=self._sensor.data.heat_stable,
                    timestamp=timestamp,
                )
            )

        return return_value
