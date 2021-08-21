import base64
import requests
import json
import time
import traceback

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


    def update_sensor_data(self, device_id, device_name, device_description, sensors = []):

        converted_list = []
        for sensor in sensors:
            converted_list.append({
                "name": sensor.name,
                "type": sensor.type,
                "value": sensor.value,
                "isAvailble": sensor.isAvailble,
                "isHealthy": sensor.isHealthy,
                "groupName": "Default",
                "settings" : None,
                "readTime": None if sensor.readTime is None else sensor.readTime.isoformat()  
            })

        payload = {
            "deviceId": device_id,
            "name": device_name,
            "description": device_description,
            "sensors": converted_list
        }  
        
        try:
            url = f"{self.base_url}/api/Device/UpdateSensorData/{device_id}"
            response = requests.request("PUT", url, data=json.dumps(payload), headers=self.headers)

            if response.status_code != 200:
                raise LookupError(f'Failed to complete the request. Error Code [{response.status_code}]')

        except:
            ex = traceback.format_exc()
            self.logger.error(f"Failed to update sensor data. Error details >> {ex}")

        return response.json()
        