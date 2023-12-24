# Handles api calls with the HydAPI api
# See documentation here: https://hydapi.nve.no/UserDocumentation

import requests
from pprint import pprint

HYDAPI_KEY = 'gdRELO4x7UuOpTzNNNCcTw==' # Yey, hardcoding a api key. Safety is me!

class HydAPI:
    '''Class that holds all the NVE Hydrological API (HydAPI) functions'''

    def get_all_stations():
        '''Returns a list of all stations'''
        url = "https://hydapi.nve.no/api/v1/Stations"

        # Headers with the API key.
        headers = {"accept": "application/json", 
                   "X-API-Key": HYDAPI_KEY}

        # Make the API request.
        response = requests.get(url, headers=headers)
    
        # Check for a successful response.
        if response.status_code == 200:
            stations = response.json()
            print(len(stations))
            for station in stations['data']:
                pprint(station)
                
        return None
    
    def get_stations_around_point(lat:float, lon:float, radius:float) -> list[dict]:
        '''Returns the stations around a pint'''
        url = "https://hydapi.nve.no/api/v1/Stations"
        headers = {"accept": "application/json", 
                   "X-API-Key": HYDAPI_KEY, 
                   "Polygon":polygon_from_point(lat, lon, radius)}
        response = requests.get(url, headers=headers)
    
        # Check for a successful response.
        if response.status_code == 200:
            stations = response.json()
            #print(stations)
            for station in stations['data']:
                pprint(station)

        return None


import math

def polygon_from_point(lat:float, long:float, radius:float, sides:int=6) -> str:
    """
    Generate a WKT polygon for a circle, hexagon, or heptagon.

    :param lat: latitude
    :param long: longitude
    :param radius: radius of the polygon in degrees
    :param sides: number of sides (6 for hexagon, 7 for heptagon)
    :return: string with WKT polygon
    """

    if sides not in [6, 7]:
        raise ValueError("Number of sides must be 6 (hexagon) or 7 (heptagon).")

    # Function to calculate the coordinates of a point on a circle
    def calculate_point(lat, long, radius, angle_deg):
        angle_rad = math.radians(angle_deg)
        lat_new = lat + (radius / 111.32) * math.cos(angle_rad)
        long_new = long + (radius / (111.32 * math.cos(math.radians(lat)))) * math.sin(angle_rad)
        return lat_new, long_new

    # Generate polygon points
    polygon_points = []
    for i in range(sides):
        angle = 360 * i / sides
        point = calculate_point(lat, long, radius, angle)
        polygon_points.append(point)

    # Add the first point to close the polygon
    polygon_points.append(polygon_points[0])

    # Format WKT polygon
    wkt_polygon = "POLYGON((" + ",".join([f"{point[1]} {point[0]}" for point in polygon_points]) + "))"

    return wkt_polygon


if __name__=='__main__':
    polygon = polygon_from_point(lat=59.911491, long=10.757933, radius=0.7) # Oslo¨
    
    print(polygon)
    x = HydAPI
    x.get_stations_around_point(lat=59.911491, lon=10.757933, radius=0.01)
    #x.get_all_stations()
