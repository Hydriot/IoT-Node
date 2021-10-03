import base64
import requests
import json
import time
import traceback

from triggers.contracts.dose_relay_abstract import DoseRelayAbstract
from triggers.contracts.on_off_relay_abstract import OnOffRelayAbstract
from common.trigger import TriggerType
from utilities.logger import Logger

class HydriotAdapter():
    driver = None
    headers = None
    logger = None

    def __init__(self, base_url, username, password) -> None:
        basic_auth = self.build_auth(username, password)
        self.base_url = base_url
        self.logger = Logger()
        
        self.headers = {
            'authorization': f"Basic {basic_auth}",
            'cache-control': "no-cache",
            'content-type': "application/json"
        }

    def build_auth(self, username, password):
        raw = f"{username}:{password}"        
        message_bytes = raw.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message
    
    def check_if_device_is_registered(self, device_id):
        try:
            url = f"{self.base_url}/api/Device/CheckRegisteredStatus/{device_id}"
            response = requests.request("GET", url, headers=self.headers)

            if response.status_code != 200:                
                raise LookupError(f'Failed to complete the request. Error Code [{response.status_code}]')

        except:
            ex = traceback.format_exc()
            self.logger.error(f"Failed to verify registration. Error details >> {ex}")
     
        return response.text == 'true'

    def register_device(self, name, description, createUpdate = False):

        payload = {
              "deviceName": name,
              "deviceDescription": description,
              "createUpdate": createUpdate
        }

        try:
            url = f"{self.base_url}/api/Device/RegisterDevice"
            response = requests.request("POST", url, data=json.dumps(payload), headers=self.headers)

            if response.status_code != 200:
                raise LookupError(f'Failed to complete the request. Error Code [{response.status_code}]')

        except:
            ex = traceback.format_exc()
            self.logger.error(f"Failed to register device. Error details >> {ex}")

        return response.json()

    def get_device_data(self, device_id):
        
        try:
            url = f"{self.base_url}/api/Device/GetDeviceData/{device_id}"
            response = requests.request("GET", url, headers=self.headers)

            if response.status_code != 200:
                raise LookupError(f'Failed to complete the request. Error Code [{response.status_code}]')

        except:
            ex = traceback.format_exc()
            self.logger.error(f"Failed to get device details. Error details >> {ex}")

        return response.json()

    
    def convert_trigger(self, trigger, trigger_type):
        default_on_state = None
        is_currently_on = trigger.check_if_switched_on()

        if (issubclass(type(trigger), DoseRelayAbstract)):        
            default_on_state = False
        
        if (issubclass(type(trigger), OnOffRelayAbstract)):
            default_on_state = trigger._is_normally_on

        code = f"{trigger.name[0:3]}01"
        trigger_type = "RelayDefaultOn" if default_on_state else "RelayDefaultOff"
        currently_on = "On" if is_currently_on else "Off"

        settings = None

        if trigger_type == TriggerType.WaterPumpCutout:
            settings = {
                "durationConfigurable": False
            }
        elif trigger_type == TriggerType.NutrientDose:
            settings = {
                "durationConfigurable": True,
                "MaxDuration": {
                    "value": 20,
                    "type": "Minutes"
                }
            }
        elif trigger_type == TriggerType.PhDose:
            settings = {
                "durationConfigurable": True,
                "MaxDuration": {
                    "value": 5,
                    "type": "Minutes"
                }
            }

        converted_trigger = {
            "name": trigger.name,                
            "code": code,
            "type": trigger_type,
            "status": currently_on,
            "settings": settings                        
        }
        
        return converted_trigger

    def syncronize_triggers(self, device_id, triggers = dict()):
        converted_list = []       

        self.logger.info(f"Trigger Payload count [{len(triggers)}]")
        for key in triggers:
            trigger = triggers[key]
            converted = self.convert_trigger(trigger, key)
            converted_list.append(converted)        

        try:
            url = f"{self.base_url}/api/Device/SyncronizeTriggers/{device_id}"
            response = requests.request("POST", url, data=json.dumps(converted_list), headers=self.headers)

            if response.status_code != 200:
                raise LookupError(f'Failed to complete the request. Error Code [{response.status_code}]')

        except:
            ex = traceback.format_exc()
            self.logger.error(f"Failed to update sensor data. Error details >> {ex}")

        return response.json()


    def update_sensor_data(self, device_id, sensors = []):

        converted_list = []
        for sensor in sensors:
            converted_list.append({
                "value": sensor.value,                
                "type": sensor.type,
                "readTime": None if sensor.readTime is None else sensor.readTime.isoformat(),                
                "name": sensor.name,
                "reference": None,
                "isAvailble": sensor.isAvailble,
                "isHealthy": sensor.isHealthy,
                "groupName": "Default",
                "settings" : None                 
            })
        
        try:
            url = f"{self.base_url}/api/Device/UpdateSensorData/{device_id}"
            response = requests.request("PUT", url, data=json.dumps(converted_list), headers=self.headers)

            if response.status_code != 200:
                raise LookupError(f'Failed to complete the request. Error Code [{response.status_code}]')

        except:
            ex = traceback.format_exc()
            self.logger.error(f"Failed to update sensor data. Error details >> {ex}")

        return response.json()
        