import requests

GTS_START_DAY = 17
GTS_START_MONTH = 12

GTS_END_DAY = 30
GTS_END_MOTNH = 12



class GridTimeSeriesAPI:
    '''Contains functionality to ask the GTS API
        See: https://api.nve.no/doc/gridtimeseries-data-gts
    '''

    @staticmethod
    def get_snow_from_point(lon:float, lat:float, year:int=2023):
        '''Returns the snow from a point'''