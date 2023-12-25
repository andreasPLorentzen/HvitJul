from enum import Enum

class SnowLevel(Enum):
    ERROR = "error"
    NONE = 0
    TRACE = 1
    LIGHT = 2
    MODERATE = 3
    HEAVY = 4
    SEVERE = 5
