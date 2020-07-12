import tempfile

from nucuhub.sensors.modules import CpuTemperature


def test_cpu_temperature_read(redis_fixture):
    with tempfile.NamedTemporaryFile(mode="w") as f:
        f.writelines("13000")
        f.flush()

        sensor = CpuTemperature()
        sensor.file_name = f.name
        sensor.enable()
        data = sensor.get_data()
        assert data is not None
