from enum import Enum
from common.sensor import SensorType
from common.trigger import TriggerType

class Hydriot():
    sensors = []
    triggers = dict()

    def set_sensor(self, sensor):
        found = False
        for index in range(len(self.sensors)):
            if (self.sensors[index].sensor_type == sensor.sensor_type):
                self.sensors[index] = sensor
                found = True
                break
            
        if not found:
            self.sensors.append(sensor)

    def get_sensor(self, sensor_type):
        for sensor in self.sensors:
            if sensor.sensor_type == sensor_type:
                return sensor

        return None

    def set_trigger(self, trigger_type, trigger):
        self.triggers[trigger_type] = trigger

    def get_trigger(self, trigger_type):
        if trigger_type not in self.triggers:
            return None
        return self.triggers[trigger_type]

    @property
    def ph_sensor(self):
        return self.get_sensor(SensorType.pH)

    @property
    def tds_sensor(self):
        return self.get_sensor(SensorType.TDS)

    @property
    def water_level_sensor(self):
        return self.get_sensor(SensorType.WaterLevel)
    
    @property
    def voltage_sensor(self):
        return self.get_sensor(SensorType.Voltage)

    @property
    def temperature_sensor(self):
        return self.get_sensor(SensorType.Temperature)

    @property
    def nutrient_trigger(self):
        return None if TriggerType.NutrientDose not in self.triggers else self.triggers[TriggerType.NutrientDose]
    
    @property
    def ph_trigger(self):
        return None if TriggerType.PhDose not in self.triggers else self.triggers[TriggerType.PhDose]

    @property
    def water_pump_trigger(self):
        return None if TriggerType.WaterPumpCutout not in self.triggers else self.triggers[TriggerType.WaterPumpCutout]