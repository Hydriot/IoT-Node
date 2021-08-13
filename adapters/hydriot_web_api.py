import requests
import json
import sys
import time

from datetime import date
from settings.app_config import AppConfig
from utilities.console_manager import ConsoleManager

class WebClient(object):
    base_url = "n/a"

    def __init__(self):
        self.base_url = AppConfig().get_integration_api_base_url()

    def show_api_result_details(self, result):
        print (f"Result code: {result.status_code}")
        if result.status_code == 200:
            print (self.get_json_text(result.json()))
        print (result.headers)
        print ("==================================================================")
        print()

    def get_json_text(self, obj):
        # create a formatted string of the Python JSON object
        return json.dumps(obj, sort_keys=True, indent=4)

    def get_json_object(self, obj):
        # create a json object that can be traversed
        return json.loads(self.get_json_text(obj))

    def transform_request_object(self, sensor_list):
        sensors = []

        for key in sensor_list:
            sensor = sensor_list[key]
            sensors.append({
                "name": sensor._name,
                "value": sensor.read_value()
            })

        data = {
            "name": "Home Node",
            "description": "string",
            "deviceId": "19be05b8-2201-40d8-9945-edc4da8fd9f1",
            "sensors": sensors
        }              

        return data
    
    def upload_sensor_readings(self, sensor_data, node_id):
        url = f"{self.base_url}/api/node/UpdateSensorData/{node_id}"
        data = self.transform_request_object(sensor_data)

        username = AppConfig().get_integration_api_username()
        password = AppConfig().get_integration_api_password()

        success = False

        try:
            print("Updating server over API...")

            # TODO: Remove verify=False before deploying to production (Local Testing Only)
            response = requests.put(url, json=data, auth=(username, password), timeout=8, verify=False)

            if response.status_code == 200:
                success = True

        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(f"Failed to update sensor readings. Error details >> {e}")
            # Sleep for 2s so that message is visible
            time.sleep(2)

            #raise SystemExit(e)           

        return success