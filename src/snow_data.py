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
    swe: float = field(default=0) # Snow Water Equvilant - Snømengde i cm
    swechange7d: float = field(default=0) # Snow Water Equvilant - Snømengde i cm - Endring siste 7 dager
    age: float = field(default=0) # Snøens Alder
    lwc: float = field(default=0) # Snøtilstand 
    fsw: float = field(default=0) # Nysnø siste døgn i cm
    fsw7d: float = field(default=0) # Nysnø siste 7 døgn i cm
    sdfsw: float = field(default=0) # Nysnødybde i cm
    qsw: float = field(default=0) # Snøsmelting siste døgn i cm


    def snow_level(self) -> bool:
        if not self.success: return SnowLevel.ERROR
        if self.sd > 80: return SnowLevel.SEVERE
        if self.sd > 40: return SnowLevel.HEAVY
        if self.sd > 14: return SnowLevel.MODERATE
        if self.sd > 2: return SnowLevel.LIGHT
        if self.sd > 0.2: return SnowLevel.TRACE
        return SnowLevel.NONE
    
    def set_value(self, key: str, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise AttributeError(f"{key} is not a valid attribute of {type(self).__name__}")
    
    def as_dict(self) -> dict:
        """Return a dictionary representation of the dataclass instance."""
        return asdict(self)