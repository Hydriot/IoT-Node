from utilities.maths import Math
from sensors.contracts.sensor_base import SensorBase
from drivers.dht22_temperature_sensor import Dh22TemperatureDriver
from settings.app_config import AppConfig
from common.sensor import SensorType

class TemperatureSensorStub(SensorBase):

    def __init__(self):
        enabled = AppConfig().is_temperature_sensor_enabled()
        SensorBase.__init__(self, None, SensorType.Temperature, "Temperature Sensor", 2, enabled, False)

    def read_implimentation(self):
        ## Stubbed Reading
        reading = Math().random_number(150, 300)
        return reading
    
    def is_available(self): 
        return True

class TemperatureSensor(SensorBase):
    driver = None
    gpio_pin = 25

    def convert_raw(self, raw_value):  
        return round(raw_value, 2)

    def __init__(self):
        enabled = AppConfig().is_tds_enabled_sensor()
        self.driver = Dh22TemperatureDriver(self.gpio_pin)
        SensorBase.__init__(self, self.driver, SensorType.Temperature, "Temperature Sensor", 2, enabled, False)
        self.sensor_summary.define_health_parameters(False, -2, 80)


