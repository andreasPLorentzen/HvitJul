
from datetime import date
from dataclasses import dataclass, field, asdict

from .snow_level import SnowLevel

@dataclass(order=True)
class SnowData:
    date: date # datetime.date
    longitude: float = field(default=None)
    latitude: float = field(default=None)
    success: bool = field(default=False)

    tm: float = field(default=0) # Tempratur i *C
    sd: float = field(default=0) # Snødybde i cm
    swe: float = field(default=0) #
    swechange7d: float = field(default=0)
    age: float = field(default=0)
    lwc: float = field(default=0)
    fsw: float = field(default=0)
    fsw7d: float = field(default=0)
    sdfsw: float = field(default=0)
    qsw: float = field(default=0)


    def snow_level(self) -> bool:
        if self.sd > 100: return SnowLevel.SEVERE
        if self.sd > 50: return SnowLevel.HEAVY
        if self.sd > 7: return SnowLevel.MODERATE
        if self.sd > 3: return SnowLevel.LIGHT
        if self.sd > 0.5: return SnowLevel.TRACE
        return SnowLevel.NONE
    
    def set_value(self, key: str, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise AttributeError(f"{key} is not a valid attribute of {type(self).__name__}")
    
    def as_dict(self) -> dict:
        """Return a dictionary representation of the dataclass instance."""
        return asdict(self)