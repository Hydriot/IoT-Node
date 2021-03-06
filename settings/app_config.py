import os
import configparser
import time

class AppConfig(object):
    _configfile_name = "config.ini"

    # sections
    environment_section = "environment"
    logging_section = "log"
    integration_api_section = "integration_api"
    sensors_section = "sensors"    
    available_sensors = "enabled_sensors"
    available_triggers = "enabled_triggers"
    
    def __init__(self):

        # Check if there is already a configuration file
        if not os.path.isfile(self._configfile_name):
            # Create the configuration file as it doesn't exist yet
            cfgfile = open(self._configfile_name, "w")

            # Add content to the file
            config = configparser.ConfigParser()

            config.add_section(self.environment_section)
            config.set(self.environment_section, "enable_sim", "false")
            config.set(self.environment_section, "safe_shutdown_threshold", "11")
            config.set(self.environment_section, "name", "Hydriot IoT Device")

            config.add_section(self.logging_section)
            config.set(self.logging_section, "enable_file_logging", "true")
            config.set(self.logging_section, "file_path", "output.log")

            config.add_section(self.available_sensors)
            config.set(self.available_sensors, "water_level_enabled", "false")
            config.set(self.available_sensors, "ph_enabled", "false")
            config.set(self.available_sensors, "tds_enabled", "false")
            config.set(self.available_sensors, "light_enabled", "false")
            config.set(self.available_sensors, "voltage_enabled", "false")
            config.set(self.available_sensors, "temperature_enabled", "false")

            config.add_section(self.available_triggers)
            config.set(self.available_triggers, "ph_down_enabled", "false")
            config.set(self.available_triggers, "nutrient_dispenser_enabled", "false")
            config.set(self.available_triggers, "water_pump_enabled", "false")

            config.add_section(self.sensors_section)
            config.set(self.sensors_section, "ph_offset", "-4.21")            

            config.add_section(self.integration_api_section)
            config.set(self.integration_api_section, "base_url", "https://hydriot.azurewebsites.net")
            config.set(self.integration_api_section, "device_id", "n/a")
            config.set(self.integration_api_section, "user", "****")
            config.set(self.integration_api_section, "pass", "****")
            config.set(self.integration_api_section, "enabled", "false")
           
            config.write(cfgfile)
            cfgfile.close()
    
    def get_key_value(self, section, key):
        config = configparser.ConfigParser() 
        cfgfile = config.read(self._configfile_name)
        return config[section][key]

    def set_key_value(self, section, key, value):
        file = open(self._configfile_name)
        parser = configparser.ConfigParser()
        parser.read_file(file)
        parser.set(section, key, value)
        new_value = parser.get(section, key)
        parser.write(open(self._configfile_name, 'w'))
       
        return new_value

    def get_enable_sim(self):
        return self.get_key_value(self.environment_section, "enable_sim") == "true"

    def get_safe_shutdown_threshold(self):
        return float(self.get_key_value(self.environment_section, "safe_shutdown_threshold"))

    def get_name(self):
        return self.get_key_value(self.environment_section, "name")

    def get_log_to_file(self):
        return self.get_key_value(self.logging_section, "enable_file_logging") == 'true'

    def get_log_file_path(self):
        return self.get_key_value(self.logging_section, "file_path")

    def get_integration_device_id(self):
        return self.get_key_value(self.integration_api_section, "device_id")

    def set_integration_device_id(self, value):        
        return self.set_key_value(self.integration_api_section, "device_id", value)

    def get_integration_api_base_url(self):
        return self.get_key_value(self.integration_api_section, "base_url")

    def get_integration_api_username(self):
        return self.get_key_value(self.integration_api_section, "user")

    def get_integration_api_password(self):
        return self.get_key_value(self.integration_api_section, "pass")

    def get_integration_enabled(self):
        return self.get_key_value(self.integration_api_section, "enabled") == "true"

    def get_ph_offset(self):
        string_value = self.get_key_value(self.sensors_section, "ph_offset")
        converted = float(string_value)
        return converted

    def is_water_level_sensor_enabled(self):
        return self.get_key_value(self.available_sensors, "water_level_enabled") == "true"

    def is_ph_enabled_sensor(self):
        return self.get_key_value(self.available_sensors, "ph_enabled") == "true"

    def is_tds_enabled_sensor(self):
        return self.get_key_value(self.available_sensors, "tds_enabled") == "true"

    def is_light_enabled_sensor(self):
        return self.get_key_value(self.available_sensors, "light_enabled") == "true"

    def is_voltage_tester_enabled(self):
        return self.get_key_value(self.available_sensors, "voltage_enabled") == "true"

    def is_temperature_sensor_enabled(self):
        return self.get_key_value(self.available_sensors, "temperature_enabled") == "true"

    def is_ph_down_enabled(self):
        return self.get_key_value(self.available_triggers, "ph_down_enabled") == "true"

    def is_nutrient_dispenser_enabled(self):
        return self.get_key_value(self.available_triggers, "nutrient_dispenser_enabled") == "true"

    def is_water_pump_enabled(self):
        return self.get_key_value(self.available_triggers, "water_pump_enabled") == "true"

