
from settings.app_config import AppConfig

from sensors.water_level_sensor import WaterLevelSensor
from sensors.ph_sensor import PhSensor
from sensors.tds_sensor import TDSSensor
from sensors.temperature_sensor import TemperatureSensor
from sensors.voltage_tester import VoltageTester

import unittest
import traceback

class SensorTests(unittest.TestCase):
    config = None

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.config = AppConfig()


    def test_water_level_sensor(self):
        is_enabled = self.config.is_water_level_sensor_enabled()

        if (not is_enabled):
            self.assertTrue()
            pass

        try:            
            sensor = WaterLevelSensor()
            value = sensor.read_value()
            print(f"Reading [{value}]")

        except:
            ex = traceback.format_exc()
            self.logger.error(f"Failed to get sensor reading [Water Level]. Error Details >> {ex}")            
            self.assertFalse()
        
        self.assertIsNotNone(value)
        self.assertTrue(value == 1 or value == 0, "Invalid value for sensor")


    def test_ph_sensor(self):
        is_enabled = self.config.is_ph_enabled_sensor()

        if (not is_enabled):
            self.assertTrue()
            pass

        try:            
            sensor = PhSensor()
            value = sensor.read_value()
            print(f"Reading [{value}]")

        except:
            ex = traceback.format_exc()
            self.logger.error(f"Failed to get sensor reading [pH]. Error Details >> {ex}")            
            self.assertFalse()
        
        self.assertIsNotNone(value)
        self.assertTrue(value > -1 and value < 15, "Invalid value for sensor")


    def test_tds_sensor(self):
        is_enabled = self.config.is_tds_enabled_sensor()

        if (not is_enabled):
            self.assertTrue()
            pass

        try:            
            sensor = TDSSensor()
            value = sensor.read_value()
            print(f"Reading [{value}]")

        except:
            ex = traceback.format_exc()
            self.logger.error(f"Failed to get sensor reading [TDS]. Error Details >> {ex}")            
            self.assertFalse()
        
        self.assertIsNotNone(value)
        self.assertTrue(value >= 0 and value < 500, "Invalid value for sensor")


    def test_temperature_sensor(self):
        is_enabled = self.config.is_temperature_sensor_enabled()

        if (not is_enabled):
            self.assertTrue()
            pass

        try:            
            sensor = TemperatureSensor()
            value = sensor.read_value()
            print(f"Reading [{value}]")

        except:
            ex = traceback.format_exc()
            self.logger.error(f"Failed to get sensor reading [Temperature]. Error Details >> {ex}")            
            self.assertFalse()
        
        self.assertIsNotNone(value)
        self.assertTrue(value >= -5 and value < 40, "Invalid value for sensor")


    def test_voltage_sensor(self):
        is_enabled = self.config.is_voltage_tester_enabled()

        if (not is_enabled):
            self.assertTrue()
            pass

        try:            
            sensor = VoltageTester()
            value = sensor.read_value()
            print(f"Reading [{value}]")

        except:
            ex = traceback.format_exc()
            self.logger.error(f"Failed to get sensor reading [Voltage]. Error Details >> {ex}")            
            self.assertFalse()
        
        self.assertIsNotNone(value)
        self.assertTrue(value >= 0 and value < 24, "Invalid value for sensor")