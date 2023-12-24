

import streamlit as st
import math
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium

# MAP settings
INPUT_MAP_CENTER = [60.0, 10.0]
INPUT_MAP_WIDTH = 1000
INPUT_MAP_HEIGHT = 600
INPUT_MAP_ZOOM = 8

def polygon_from_point(lat:float, long:float, radius:float, sides:int=6) -> str:
    """
    Generate a WKT polygon for a circle, hexagon, or heptagon.

    :param lat: latitude
    :param long: longitude
    :param radius: radius of the polygon in meters
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
        return round(lat_new,3), round(long_new,3)

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

def draw_trip_in_map():
    map_center = INPUT_MAP_CENTER


    m = folium.Map(location=INPUT_MAP_CENTER, zoom_start=INPUT_MAP_ZOOM, max_zoom=17, min_lat=10, min_lon=3, max_lon=35, auto_save=False, export=False)

    # NOT REALLY A GOOD WAY, but all other attempts seems to fail...

    for tilematrix_level in range(4, 17):
        tiles = f"https://cache.kartverket.no/topo/v1/wmts/1.0.0/?layer=topo&style=default&tilematrixset=googlemaps&Service=WMTS&Request=GetTile&Version=1.0.0&Format=image%2Fpng&TileMatrix={tilematrix_level}" + "&TileCol={x}&TileRow={y}"

        wmts_layer = folium.TileLayer(
            tiles=tiles,
            attr="Kartverket",
            name="WMTS Layer",
            overlay=True,
            control=True,
            # tms=True,  # If using TMS tiling set this to True
            # tilematrix='EPSG:3857'  # Change to the appropriate tile matrix if necessary
        ).add_to(m)

        draw = Draw(
            export=True,
            draw_options={
                'polyline': False,
                'polygon': False,  # Disables drawing Polygons
                'circle': False,  # Disables drawing Circles
                'rectangle': False,  # Disables drawing Rectangles
                'marker':  {'shapeOptions': {
                        'color': '#b81c21',  # Line color
                        'weight': 4,  # Line weight
                        'opacity': 1.0,  # Line opacity (0.0 to 1.0)
                    },}
                ,  # Disables placing Markers
                'circlemarker': False,  # Disables placing Circle Markers
            },
            edit_options={
                'featureGroup': None,
                # You must define a FeatureGroup for editing (or it will create an empty one for use)
                'remove': False,  # Allow removing shapes
                'edit': True  # Allow editing shapes
            },
        )


    data = st_folium(m, height=INPUT_MAP_HEIGHT, width=INPUT_MAP_WIDTH)


    return data

def wrapper_page():
    # st.set_page_config(layout="wide")

    data = draw_trip_in_map()
    st.write(data)
    st.write(data["last_clicked"])

    if data["last_clicked"] is not None:
        polygon =polygon_from_point(data["last_clicked"]["lat"], data["last_clicked"]["lng"], 1)
        st.write(polygon)


class nve_data():
    def __init__(self):
        def



if __name__ == "__main__":
    wrapper_page()