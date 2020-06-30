import abc
import typing

from nucuhub.domain.sensors import SensorMeasurement, SensorState
from nucuhub.domain.sensors.config import SensorConfig
from nucuhub.logging import get_logger
from nucuhub.sensors.infrastructure import Database


class SensorException(Exception):
    pass


class SensorModule(abc.ABC):
    _config: SensorConfig = None
    _db: Database = Database()
    _logger = get_logger("SensorModule")

    def __init__(self):
        self._initialize()

    def _save_config(self):
        if self._config:
            self._db.save_config(self._config.id, self._config.__dict__)

    def _load_config(self):
        old_config = self._db.load_config(self._config.id)
        if old_config:
            self._config = SensorConfig(**old_config)

    def _initialize(self):
        self._config = self._configure()
        self._load_config()
        # Custom logic to be implemented in sub-classes.

    def _configure(self) -> SensorConfig:
        """
            Should return an instance of SensorConfig.
        """
        raise NotImplementedError()

    def _get_data(self) -> typing.List[SensorMeasurement]:
        """
            Performs a read from the sensor.
        :return: A list of SensorMeasurement.
        """
        raise NotImplementedError()

    @property
    def id(self) -> str:
        return self._config.id

    @property
    def name(self) -> str:
        """
            Returns a friendly name for the sensor.
        """
        return self._config.name

    @property
    def description(self) -> str:
        """
            Returns the sensor's description.
        """
        return self._config.description

    @property
    def is_enabled(self) -> bool:
        """
            Queries if the sensor is enabled or not.
        """
        return self._config.enabled

    @property
    def state(self) -> str:
        """
            Queries the state the sensor is in. Valid states are defined in the SensorState enum.
        """
        return self._config.state

    def get_data(self) -> typing.List[SensorMeasurement]:
        """
            Performs a sensor read and returns the data.
        """
        if not self._config.enabled:
            raise SensorException(
                "Invalid operation: performing read on disabled sensor."
            )
        return self._get_data()

    def enable(self):
        """
            Enables the sensor.
        """
        if not self._config.enabled:
            self._config.enabled = True
            self._save_config()

    def disable(self):
        """
            Disables the sensor.
        """
        if self._config.enabled:
            self._config.enabled = False
            self._save_config()

    def set_state(self, sensor_state: SensorState):
        """
            Sets the sensor state.
        """
        self._config.state = sensor_state.value
        self._save_config()
