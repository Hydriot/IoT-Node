import traceback

from settings.app_config import AppConfig
from datetime import datetime
from utilities.logger import Logger

class ConsoleManager(object):
    toggle = True
    logger = None

    def __init__(self):
        self.logger = Logger()     

    def get_sensor_summary(self, sensor_summary):
        age_in_seconds = None if sensor_summary.last_execution is None else round((datetime.utcnow() - sensor_summary.last_execution).total_seconds(), 0)
        latest_value = None if sensor_summary.latest_value is None else sensor_summary.latest_value
        default_display = "n/a"

        summary = f"{sensor_summary.name} latest reading is "
        summary += "[" + ("~" if sensor_summary.is_stabilizing else "")
        summary += (default_display if latest_value is None else str(latest_value)) + "] "
        summary += "from [" + (default_display if age_in_seconds is None else str(age_in_seconds)) + "] seconds ago. "
        summary += "AVG [" + (default_display if sensor_summary.average_reading is None else str(round(sensor_summary.average_reading,2))) + "] "
        summary += "DEV [" + (default_display if sensor_summary.reading_deviation is None else str(round(sensor_summary.reading_deviation,2))) + "] "
        summary += ">>> " + ("HEALTHY" if sensor_summary.is_healthy() else "UNHEALTHY") + " <<<"

        return summary

    def get_trigger_summary(self, trigger):
        current_on_status = trigger.check_if_switched_on()
        status = "On" if current_on_status else "Off"
        summary = f"{trigger.name} is switched [{status}]"
        
        return summary

    def display_sensors(self, hydriot, integration_adapter, task_manager):
        try:        
            Logger.clear_console()
            config = AppConfig()

            self.logger.console("Hydriot Node")
            self.logger.console("=====================================================")
            self.logger.console("")

            self.logger.console(">>> Registered Sensors <<<")

            if hydriot.tds_sensor is not None:
                self.logger.console(self.get_sensor_summary(hydriot.tds_sensor))
            if hydriot.water_level_sensor is not None:
                self.logger.console(self.get_sensor_summary(hydriot.water_level_sensor))
            if hydriot.ph_sensor is not None:
                self.logger.console(self.get_sensor_summary(hydriot.ph_sensor))
            if hydriot.voltage_sensor is not None:
                self.logger.console(self.get_sensor_summary(hydriot.voltage_sensor))

            self.logger.console("")
            self.logger.console(">>> Registered Triggers <<<")

            if hydriot.water_pump_trigger is not None and hydriot.water_pump_trigger.is_enabled:
                self.logger.console(self.get_trigger_summary(hydriot.water_pump_trigger))

            if hydriot.nutrient_trigger is not None and hydriot.nutrient_trigger.is_enabled:
                self.logger.console(self.get_trigger_summary(hydriot.nutrient_trigger))
            
            if hydriot.ph_trigger is not None and hydriot.ph_trigger.is_enabled:
                self.logger.console(self.get_trigger_summary(hydriot.ph_trigger))

            self.logger.console()
            self.logger.console(">>> Integration Status <<<")
            status = "Connected" if integration_adapter.previous_integration_success else "Disconnected"
            last_update = "N/A" if integration_adapter.last_integration_update == None else integration_adapter.last_integration_update
            self.logger.console(f"Connection status: [{status}] last updated [{last_update}]")

            self.logger.console()
            if config.get_enable_sim():
                self.logger.console("WARNING! Simulator Mode Enabled")
                pass

            task_list = ""
            for key in task_manager.tasks:
                task_list += f"[{key}] "

            self.logger.console(f"Active tasks: {task_list}")
                            
            self.logger.console("----------------------------------------------------")    
            footer = "*Press Cntr+C to exit monitoring "
            footer += "[-]" if self.toggle else "[|]"
            self.logger.console(footer)
            self.logger.console("")

            self.toggle = not self.toggle

        except:
            ex = traceback.format_exc()
            self.logger.error(f"Failed to do refresh and display the latest node stats. Error Details >> {ex}")
        

