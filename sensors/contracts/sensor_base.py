import asyncio
import traceback

from common.sensor_summary import SensorSummary
from common.scheduling_abstract import SchedulingAbstract
from utilities.logger import Logger

class SensorBase(SchedulingAbstract):    
    sensor_summary = None
    driver = None
    is_enabled = None
    logger = None
    
    def __init__(self, driver, type, sensor_name, frequency_in_seconds, is_enabled = False, use_average = False):
        self.driver = driver
        self.sensor_summary = SensorSummary(sensor_name, type, frequency_in_seconds)
        self.is_enabled = is_enabled
        SchedulingAbstract.__init__(self, frequency_in_seconds, sensor_name, use_average)
        self.sensor_type = type
        self.logger = Logger()

    def get_last_read_time(self):
        return self.sensor_summary.last_execution
    
    def get_latest_value(self):
        return self.sensor_summary.current_value

    def convert_raw(self, raw_value):
        return raw_value

    async def read_average(self, count, delay_in_milliseconds):
        try:
            total = 0        

            for i in range(count):
                value = self.read_raw()
                total += value
                if delay_in_milliseconds > 0:
                    await asyncio.sleep(delay_in_milliseconds/1000)          

            average = total / count
            converted = self.convert_raw(average)
            self.sensor_summary.update_value(converted)
            return converted
        
        except:
            ex = traceback.format_exc()
            self.sensor_summary.set_last_read_error()
            self.logger.error(f"Failed to read [{self.sensor_summary.name}]. Error Details >> {ex}")
            return None

    ## Override if needed
    def post_read_action(self):
        pass

    def read_value(self):

        try:
            value = self.read_raw()
            converted = self.convert_raw(value)
            self.sensor_summary.update_value(converted)
            self.post_read_action()  

            return converted

        except:
            ex = traceback.format_exc()
            self.sensor_summary.set_last_read_error()
            self.logger.error(f"Failed to read [{self.sensor_summary.name}]. Error Details >> {ex}")
            return None

    def read_raw(self):
        if self.driver is None:
            raise NotImplementedError

        return self.driver.read_value()

    def is_available(self):
        try:
            if self.driver is None:
                return False

            ## Check if there is a driver is available implimentation
            driver_self_check = self.driver.is_available()
            if driver_self_check is not None:
                return driver_self_check
            
            ## Fallback, check that we can read the raw value without an error
            self.read_raw()

            return True

        except:
            ex = traceback.format_exc()          
            self.sensor_summary.set_last_read_error()
            self.logger.error(f"Failed to verify if [{self.sensor_summary.name}] is available. Error Details >> {ex}")
            return False

