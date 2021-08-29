import traceback
import asyncio

from datetime import datetime
from adapters.hydriot_adapter import HydriotAdapter
from settings.app_config import AppConfig
from utilities.logger import Logger

class IntegrationAdapter(object):
    _frequency_in_seconds = 1    
    _is_monitoring = False
    _sensors = None
    _device_id = "n/a"
    _name = None
    last_integration_update = None
    previous_integration_success = False
    adapter = None
    logger = None

    def __init__(self, update_frequency):
        self._frequency_in_seconds = update_frequency
        base_url = AppConfig().get_integration_api_base_url()
        username = AppConfig().get_integration_api_username()
        password = AppConfig().get_integration_api_password()
        self.adapter = HydriotAdapter(base_url, username, password)
        self._device_id = AppConfig().get_integration_device_id()
        self._name = AppConfig().get_name()
        self.logger = Logger()
    
    async def register_integration(self):
        try:
            if not AppConfig().get_integration_enabled():                
                self.logger.warn("Update to hydriot online is disabled. Not scheduling sensor updates.")
                return

            self._is_monitoring = True

            # Get Registered ID or Create a new one
            if self._device_id == "n/a":
                self._device_id = self.adapter.register_device(self._name, self._name, True)
                updated_value = AppConfig().set_integration_device_id(self._device_id)
                self.logger.info(f"Updated the Device ID from Hydriot Online. DeviceID [{updated_value}]")

            while self._is_monitoring:
                await asyncio.sleep(self._frequency_in_seconds) 

                try:
                    sensor_list = []
                    for sensor in self._sensors:
                        converted_sensor = sensor.convert_online()
                        if converted_sensor is not None:
                            sensor_list.append(converted_sensor)

                    self.adapter.update_sensor_data(self._device_id, sensor_list)

                    self.previous_integration_success = True
                    self.last_integration_update = datetime.utcnow()                

                except:
                    ex = traceback.format_exc()
                    self.previous_integration_success = False                     
                    self.logger.error(f"Failed to do an update with the latest information to Hydriot online. Error Details >> {ex}")

        except:
            ex = traceback.format_exc()
            self.logger.error(f"Failed to schedule the updating of information to Hydriot online >> {ex}")

    def stop_monitoring(self):
        self._is_monitoring = False

    def start_monitoring(self, sensors):
        self._sensors = sensors
        asyncio.ensure_future(self.register_integration())  
    
    def cleanup(self):
        self.stop_monitoring()
