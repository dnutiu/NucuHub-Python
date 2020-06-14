import concurrent.futures
import importlib
import pathlib
import pkgutil
import signal
import time
import typing

from nucuhub.domain.sensors import SensorModule
from nucuhub.logging import get_logger
from nucuhub.sensors import infrastructure


class SensorsWorker:
    def __init__(self):
        self.message_broker = infrastructure.Messaging()
        self.logger = get_logger("SensorWorker")
        self.sleep_time = 1

        self._reading_loop_should_run = True
        self._command_loop_should_run = True
        self._worker_loop_should_run = True

        self.sensor_modules = self._import_sensor_modules()
        self.loaded_sensor_modules = []

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

    def _load_modules(self):
        for m in self.sensor_modules:
            self.loaded_sensor_modules.append(m())

    def _command_loop(self):
        """
            Listens to sensor config messages.
            Example:
            {
                'sensor_id': 'cpu_temperature_sensor'
                'action' 'enable/disable'
            }
        """
        while self._command_loop_should_run:
            message = self.message_broker.get_message()
            self.logger.debug(f"received cmd message: {message}")
            if message:
                sensor_id = message.get("sensor_id")
                action = message.get("action")
                if action not in ("enable", "disable"):
                    continue
                for sensor in self.loaded_sensor_modules:
                    if sensor.id == sensor_id:
                        getattr(sensor, action)()
                        self.logger.info(
                            f"ran the action '{action}' on sensor: {sensor_id}."
                        )
                        break
            time.sleep(self.sleep_time)

    def _reading_loop(self):
        """
            Loops through sensors and publises data.
        """
        while self._reading_loop_should_run:
            all_data = []
            # Iterate through all sensors and retrieve data
            for sensor in self.loaded_sensor_modules:
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
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGTSTP, self.shutdown)

        self.logger.info("Looping forever!")
        self._load_modules()

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            reading_loop = executor.submit(self._reading_loop)
            command_loop = executor.submit(self._command_loop)
            while self._worker_loop_should_run:
                try:
                    if not reading_loop.running() and self._worker_loop_should_run:
                        reading_loop.cancel()
                        self.logger.warning(
                            f"restarting reading_loop because it's not running! {reading_loop.exception(timeout=2)}"
                        )
                        reading_loop = executor.submit(self._reading_loop)
                        time.sleep(2)
                    if not command_loop.running() and self._worker_loop_should_run:
                        command_loop.cancel()
                        self.logger.warning(
                            f"restarting command_loop because it's not running! {command_loop.exception(timeout=2)}"
                        )
                        reading_loop = executor.submit(self._command_loop)
                        time.sleep(2)
                except concurrent.futures.CancelledError as e:
                    # We get a canceled error when we cancel tasks.
                    self.logger.warning(e)
                time.sleep(self.sleep_time)

    def shutdown(self, signum, frame):
        self.logger.info("Shutting down... waiting for loops to finish work.")
        self._worker_loop_should_run = False
        self._command_loop_should_run = False
        self._reading_loop_should_run = False


def main():
    s = SensorsWorker()
    s.loop_forever()


if __name__ == "__main__":
    main()
