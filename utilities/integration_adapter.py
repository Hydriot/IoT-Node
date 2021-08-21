import traceback
import asyncio

from datetime import datetime
from adapters.hydriot_adapter import HydriotAdapter
from settings.app_config import AppConfig

class IntegrationAdapter(object):
    _frequency_in_seconds = 1    
    _is_monitoring = False
    _sensors = None
    _device_id = "n/a"
    _name = None
    last_integration_update = None
    previous_integration_success = False
    adapter = None

    def __init__(self, update_frequency):
        self._frequency_in_seconds = update_frequency
        base_url = AppConfig().get_integration_api_base_url()
        username = AppConfig().get_integration_api_username()
        password = AppConfig().get_integration_api_password()
        self.adapter = HydriotAdapter(base_url, username, password)
        self._device_id = AppConfig().get_integration_device_id()
        self._name = AppConfig().get_name()
    
    async def register_integration(self):
        self._is_monitoring = True
        if_registered = None

        if self._sensors != None:
            pass

        if self._device_id == "n/a":
            self._device_id = self.adapter.register_device(self._name, self._name, True)
            AppConfig().set_integration_device_id(self._device_id)

        while self._is_monitoring and (if_registered == None or if_registered == True):
            await asyncio.sleep(self._frequency_in_seconds) 

            try:

                if (if_registered == None):
                    if_registered = self.adapter.check_if_device_is_registered(self._device_id)

                if not AppConfig().get_integration_enabled():                
                    continue

                sensor_list = []
                for sensor in self._sensors:
                    converted_sensor = sensor.convert_online()
                    if converted_sensor is not None:
                        sensor_list.append(converted_sensor)

                device_data = self.adapter.update_sensor_data(self._device_id, 'Test Device', 'Seed example device', sensor_list)

                self.previous_integration_success = True
                self.last_integration_update = datetime.now()                

            except:
                ex = traceback.format_exc()
                self.previous_integration_success = False                     
                print(f"Failed to do Update the latest information to Hydriot online. Error Details >> {ex}")


    def stop_monitoring(self):
        self._is_monitoring = False

    def start_monitoring(self, sensors):
        self._sensors = sensors
        asyncio.ensure_future(self.register_integration())  
    
    def cleanup(self):
        self.stop_monitoring()
