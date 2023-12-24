import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium

from .utils import polygon_from_point
import random

# MAP settings
INPUT_MAP_CENTER = [60.0, 10.0]
INPUT_MAP_WIDTH = 1000
INPUT_MAP_HEIGHT = 600
INPUT_MAP_ZOOM = 8

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


    write_trees({"ost":1})

def write_trees(years=dict):
    years = {
        2024: 0,
        2023: 2,
        2022: 1,
        2021: 0,
        2020: 0,
        2019: 0,
    }
    years_list = []
    for year, category in years.items():
        years_list.append((year, category))

    for row in range(0,3):
        col1,col2,col3,col4,col5,col6,col7,col8,col9,col10 = st.columns(10,gap="small")
        cols = [col1,col2,col3,col4,col5,col6,col7,col8,col9,col10]
        for col in cols:
            with col:
                st.image(f"Graphics/SNOW_{random.randint(0,2)}.png",)
                st.markdown(
                    f"<div style='text-align: center; padding-top: 0px;'>{years_list[0][0]}</div>",
                    unsafe_allow_html=True
                )
    # graphics = {
    #     0: "SNOW_0"
    # }




if __name__ == "__main__":
    wrapper_page()