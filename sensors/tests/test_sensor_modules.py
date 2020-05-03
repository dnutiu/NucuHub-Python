from sensors.modules import CpuTemperature


def test_cpu_temperature_read():
    sensor = CpuTemperature()
    sensor.enable()
    data = sensor.get_data()
    assert data is not None
