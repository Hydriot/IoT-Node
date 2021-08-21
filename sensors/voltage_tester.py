import os

from utilities.maths import Math
from sensors.contracts.sensor_base import SensorBase
from drivers.rasbee_voltage_tester import RasbeeVoltageTesterDriver
from settings.app_config import AppConfig
from common.sensor import SensorType
from utilities.logger import Logger

class VoltageTesterStub(SensorBase):
    config = AppConfig()

    def __init__(self):        
        enabled = self.config.is_voltage_tester_enabled()
        SensorBase.__init__(self, None, SensorType.VoltageTester, "Battery Voltage Tester", 2, enabled, False)

    def read_implimentation(self):
        ## Stubbed Reading
        reading = Math().random_number(0, 12)
        return reading
    
    def is_available(self): 
        return True

class VoltageTester(SensorBase):
    driver = None
    config = AppConfig()

    def __init__(self):        
        enabled = self.config.is_voltage_tester_enabled()
        self.driver = RasbeeVoltageTesterDriver()
        SensorBase.__init__(self, self.driver, SensorType.Voltage, "Battery Voltage Tester", 2, enabled, False)
        self.sensor_summary.define_health_parameters(True, 10, 14)

    def post_read_action(self):
        safe_shutdown_threshold = self.config.get_safe_shutdown_threshold()
        delay_in_seconds = 10

        if self.sensor_summary._history_depth < 10:
            return
        
        average_value = self.sensor_summary.average_reading

        if average_value > 2 and average_value < safe_shutdown_threshold:            

            for count in range(delay_in_seconds, 0, -1):
                Logger.clear_console()
                self.logger.warn(f"WARNING! Dangerously low voltage detected, shutting down the system in [{count}] seconds.", 1)

            os.system("sudo shutdown -h now")

    def convert_raw(self, raw_value):
        converter = raw_value / 199        
        return round(converter, 2)