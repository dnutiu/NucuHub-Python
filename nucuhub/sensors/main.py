import importlib
import pathlib
import pkgutil
import time
import typing

from nucuhub.domain.logging import get_logger
from nucuhub.sensors import infrastructure
from nucuhub.sensors.abstractions import SensorModule


class SensorsWorker:
    def __init__(self):
        self.message_broker = infrastructure.Messaging()
        self.logger = get_logger("SensorWorker")
        self.sleep_time = 1

        self.sensor_modules = self._import_sensor_modules()

    def _import_sensor_modules(self) -> typing.List[typing.Type[SensorModule]]:
        """
            Imports all sensor modules.
        """
        sensor_modules = []
        module_path = pathlib.Path(__file__).parent / "modules"
        for (_, submodule_name, _) in pkgutil.iter_modules([module_path]):
            module = importlib.import_module(
                f".modules.{submodule_name}", package="nucuhub.sensors"
            )
            for mod in dir(module):
                if mod.startswith("_") or mod == "SensorModule":
                    continue
                try:
                    sensor_module = getattr(module, mod)
                    if issubclass(sensor_module, SensorModule):
                        sensor_modules.append(sensor_module)
                except TypeError:
                    pass
        self.logger.debug(f"Loaded the following sensor modules: {sensor_modules}")
        return sensor_modules

    def _loop(self):
        loaded_modules = []
        for m in self.sensor_modules:
            loaded_modules.append(m())

        while True:
            all_data = []
            # Iterate through all sensors and retrieve data
            for sensor in loaded_modules:
                if sensor.is_enabled:
                    json_data = [item.__dict__ for item in sensor.get_data()]
                    all_data.extend(json_data)
            self.message_broker.publish(all_data)
            time.sleep(self.sleep_time)

    def loop_forever(self) -> None:
        """
            Looping forever.
            It polls the sensors and publishes the data to the via Messaging.
        """
        self.logger.info("Looping forever!")
        try:
            self._loop()
            # todo add loop for listening to redis for config changes
        except KeyboardInterrupt:
            self.logger.info("Shutting down...")


def main():
    s = SensorsWorker()
    s.loop_forever()


if __name__ == "__main__":
    main()
