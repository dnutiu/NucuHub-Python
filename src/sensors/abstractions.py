import abc
import typing
from dataclasses import dataclass

from src.domain.exceptions import SensorException
from src.sensors.config import SensorConfig
from src.sensors.infrastructure import Database


@dataclass
class SensorMeasurement:
    name: str
    description: str
    value: typing.Union[int, float, str]


class SensorModule(abc.ABC):
    _config: SensorConfig = None
    _db: Database = Database()

    def __init__(self):
        self._initialize()

    def _save_config(self):
        self._db.save_config(self._config.id, self._config)

    def _load_config(self):
        old_config = self._db.load_config(self._config.id)
        if old_config:
            self._config = old_config

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
            Quries if the sensor is enabled or not.
        """
        return self._config.enabled

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
