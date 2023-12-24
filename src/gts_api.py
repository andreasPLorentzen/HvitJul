import requests
from dataclasses import dataclass, field, asdict
import json
from statistics import mean 
from datetime import date
from enum import Enum

from utils import convert_coordinates

class SnowLevel(Enum):
    NONE = 0
    TRACE = 1
    LIGHT = 2
    MODERATE = 3
    HEAVY = 4
    SEVERE = 5

@dataclass(order=True)
class SnowData:
    date: date # datetime.date
    longitude: float = field(default=None)
    latitude: float = field(default=None)

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

GTS_RELEVANT_INFORMATION = {
    'tm':'temperature',
    'sd':'snow_depth',
    #'swe':'snow_weight_equivalent',
    #'swechange7d':'snow_weight_equivalent_change_last_7_days',
    #'age':'snow_age',
    #'lwc':'snow_state',
    'fsw':'new_snow_last_day',
    #'fsw7d':'new_snow_last_7_days',
    #'sdfsw':'new_snow_depth',
    #'qsw':'snow_melt_last_day',
}

class GridTimeSeriesAPI:
    '''Contains functionality to ask the GTS API
        See: https://api.nve.no/doc/gridtimeseries-data-gts
    '''

    @staticmethod
    def get_snow_info(lat:float, lon:float, year:int=2023, month:int=12, day:int=24) -> SnowData:
        '''Returns the snow from a point'''
        x, y = convert_coordinates(lat=lat, lon=lon)
        start_date = f'{year}-{month}-{day}'
        end_date = f'{year}-{month}-{day}'
        wd = SnowData(date(year, month, day), longitude=lon, latitude=lat)

        for data_type, description in GTS_RELEVANT_INFORMATION.items():
            url = f'https://gts.nve.no/api/GridTimeSeries/{int(x)}/{int(y)}/{start_date}/{end_date}/{data_type}.json'
            response = requests.get(url)
            if response.status_code == 200:
                response_dict = json.loads(response.text)
                data = mean(response_dict['Data'])
                wd.set_value(data_type, data)
        return wd

    @staticmethod
    def get_snow_info_years(lat:float, lon:float, year_start:int=2010, year_end:int=2023, month:int=12, day:int=24) -> list[SnowData]:
        years = range(year_start, year_end+1)
        wds = [GridTimeSeriesAPI.get_snow_info(lat=lat, lon=lon, year=x, month=month, day=day) for x in years]
        return wds



if __name__=='__main__':
    wd = GridTimeSeriesAPI.get_snow_info(lat=59.911491, lon=10.757933, year=2023)
    print(wd.snow_level())
    x = GridTimeSeriesAPI.get_snow_info_years(lat=59.911491, lon=10.757933)
    print(x)
    print({x.date.year:x.snow_level() for x in x})