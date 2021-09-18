from datetime import datetime
from enum import IntEnum

class BaseType(IntEnum):
    Undefined = 0
    String = 1
    Integer = 2
    Decimal = 3

class SensorType(IntEnum):
    Undefined = 0
    WaterLevel = 1
    TDS = 2
    pH = 3
    LightFrequency = 4
    LightIntensity = 5
    Voltage = 6
    Custom = 99

class Settings():
    BaseType = None
    LowerBound = None
    UpperBound = None

    def __init__(self, base_type, lower_bound, upper_bound):
        self.BaseType = base_type
        self.LowerBound = lower_bound
        self.UpperBound = upper_bound

class Sensor():
    value = None
    type = None
    readTime = None
    name = None
    reference = None
    isAvailble = True
    isHealthy = True
    groupName = None
    settings = None

    def __init__(self, type, value, read_time = datetime.now(), name = None, group_name = 'default', settings = None):
        self.name = str(type) if name is None else name
        self.value = value
        self.type = type
        self.readTime = read_time
        self.groupName = group_name
        self.settings = settings

