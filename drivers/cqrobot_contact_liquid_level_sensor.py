import wiringpi as GPIO
import traceback

from drivers.driver_base import DriverBase
from utilities.pin_converter import PinMapper
from settings.app_config import AppConfig
from utilities.logger import Logger

## Manufacturer Source
## http://www.cqrobot.wiki/index.php/Liquid_Level_Sensor

class CQRobotContactLiquidLevelSensorDriver(DriverBase):
    wiringpi_pin = None
    logger = None

    def __init__(self, gpio_pin):
        DriverBase.__init__(self)
        self.wiringpi_pin = PinMapper().gpio_to_wiringpi(gpio_pin)
        self.logger = Logger()

    def initialize(self):
        GPIO.wiringPiSetup()

    
    


    def read_value(self):
        
        

        reading = GPIO.digitalRead(self.wiringpi_pin)
        return reading

    def is_available(self):
        reading = -1

        if AppConfig().is_water_level_sensor_enabled() is False:
            return False

        try:
            # TODO: If there is nothing it still reads as 0 need better mechanism
            reading = self.read_value()
        except:
            ex = traceback.format_exc()
            self.logger.error(f"Failed to read Liquid Level Sensor. Error Details >> {ex}")
            return False
        finally:
            if reading > -1:
                return True        
        
        return False