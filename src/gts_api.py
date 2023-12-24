import requests
import json
from statistics import mean 
from datetime import date

from .utils import convert_coordinates
from .snow_data import SnowData

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