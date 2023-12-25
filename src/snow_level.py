from enum import Enum

class SnowLevel(Enum):
    ERROR = -1
    NONE = 0
    TRACE = 1
    LIGHT = 2
    MODERATE = 3
    HEAVY = 4
    SEVERE = 5
