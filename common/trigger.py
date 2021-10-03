from enum import Enum

class TriggerType(Enum):
    Undefined = 0,
    NutrientDose = 1,
    PhDose = 2,
    WaterPumpCutout = 3