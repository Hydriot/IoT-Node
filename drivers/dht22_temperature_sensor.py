import traceback
import Adafruit_DHT as dht

from drivers.driver_base import DriverBase
from settings.app_config import AppConfig
from utilities.logger import Logger


## Manufacturer Source
## https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/

class Dh22TemperatureDriver(DriverBase):
    pin = None
    last_humidity = None
    last_temperature = None    

    def __init__(self, pin): 
        DriverBase.__init__(self)       
        self.pin = pin ## GPIO PIN 

    def initialize(self):
        pass

    def read_value(self):
        self.humidity, self.temperature = dht.read_retry(dht.DHT22, self.pin)
        return self.temperature

    def is_available(self):
        reading = -1
        
        if AppConfig().is_temperature_sensor_enabled() is False:
            return False

        try:
            reading = self.read_value()
        except:
            ex = traceback.format_exc()
            self.logger.error(f"Failed to read temperature. Error Details >> {ex}")
            return False
        finally:
            if reading > -1:
                return True        
        
        return False
