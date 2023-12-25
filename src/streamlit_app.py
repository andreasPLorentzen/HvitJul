import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
from src.gts_api import GridTimeSeriesAPI

from .utils import polygon_from_point
import random, requests

# MAP settings
INPUT_MAP_CENTER = [60.0, 10.0]
INPUT_MAP_WIDTH = 1000
INPUT_MAP_HEIGHT = 600
INPUT_MAP_ZOOM = 8

def draw_trip_in_map():
    if "markers" not in st.session_state:
        st.session_state["markers"] = []
    m = folium.Map(location=INPUT_MAP_CENTER, zoom_start=INPUT_MAP_ZOOM, export=False)


    # NOT REALLY A GOOD WAY, but all other attempts seems to fail...

    # for tilematrix_level in range(4, 17):
    #     tiles = f"https://cache.kartverket.no/topo/v1/wmts/1.0.0/?layer=topo&style=default&tilematrixset=googlemaps&Service=WMTS&Request=GetTile&Version=1.0.0&Format=image%2Fpng&TileMatrix={tilematrix_level}" + "&TileCol={x}&TileRow={y}"
    #
    #     wmts_layer = folium.TileLayer(
    #         tiles=tiles,
    #         attr="Kartverket",
    #         name="WMTS Layer",
    #         overlay=True,
    #         control=True,
    #         # tms=True,  # If using TMS tiling set this to True
    #         # tilematrix='EPSG:3857'  # Change to the appropriate tile matrix if necessary
    #     ).add_to(m)

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
    draw.add_to(m)
    fg = folium.FeatureGroup(name="Markers")
    for marker in st.session_state["markers"]:
        fg.add_child(marker)
    # if data["last_clicked"] is not None:
    #     folium.Marker([data["last_clicked"]["lat"], data["last_clicked"]["lng"]]).add_to(m)


    # data = st_folium(f_m, height=INPUT_MAP_HEIGHT, width=INPUT_MAP_WIDTH,  feature_group_to_add=fg, key="new")
    data = st_folium(m, width=725)
    # data =  st_folium(m)
    # # if data["last_clicked"] is not None:
    if data.get("last_clicked"):
        marker = folium.Marker([data["last_clicked"]["lat"], data["last_clicked"]["lng"]])
        st.session_state["markers"] = [marker]
    #








    return data

def get_place_names(query):
    base_url = "https://api.kartverket.no/stedsnavn/v1/navn"
    params = {
        "sok": query,
        "fuzzy": "true",
        "utkoordsys": "4258",
        "treffPerSide": "10",
        "side": "1"
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_x_first_place_names(query, x=10) -> (list,list):
    api_request = get_place_names(query)
    return_list = []

    if api_request == []:
        return []

    # st.write(api_request["navn"])

    for index, data in enumerate(api_request["navn"]):
        # if data["navneobjekttype"]
        return_list.append(str(data["skrivemåte"]) + ", " + str(data["kommuner"][0]["kommunenavn"]))

        if index > x:
            break
    return return_list, api_request

def get_place_name(lat,long):
    url = f"https://api.kartverket.no/stedsnavn/v1/punkt?"
    base_url = "https://api.kartverket.no/stedsnavn/v1/punkt"
    params = {
        "nord": lat,
        "ost": long,
        "koordsys": 4258,
        "radius": 500,
        "fuzzy": "true",
        "utkoordsys": "4258",
        "treffPerSide": "1",
        "side": "1"
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        try:
            return response.json()["navn"][0]["stedsnavn"][0]["skrivemåte"]
        except:
            return "Stedsnavn ikke funnet."
    else:
        return "Ikke noe sted valgt."


def placenames_options(querey):
    if len(querey) < 4:
        return [""]
    return get_x_first_place_names(querey)[0]

def wrapper_page():
    # st.set_page_config(layout="wide")
    lat = None
    lon = None

    st.title("Hvor hvit er egentlig jula?")

    place_query = st.text_input("Enter a place name", "")
    if place_query:
        # place_names = get_place_names(place_query)
        # st.write(place_names)
        first_10_place_names, place_names = get_x_first_place_names(place_query, 10)
        # st.write(first_10_place_names)
        if 'navn' in place_names:
            # options = [place['navn'] for place in place_names['navn']]
            options = first_10_place_names
            st.selectbox("Select a place", options)
        else:
            st.warning("No places found for your query.")

    # test = "Tynset"
    # options = placenames_options(test)
    # test = st.selectbox("Søk på stedsnavn", placenames_options(test))
    # st.write(test)

    data = draw_trip_in_map()
    # st.write(data)
    st.write(data["last_clicked"])

    if data["last_clicked"] is not None:
        # polygon =polygon_from_point(data["last_clicked"]["lat"], data["last_clicked"]["lng"], 1)
        # st.write(polygon)
        lat = data["last_clicked"]["lat"]
        lon = data["last_clicked"]["lng"]
        location_name = get_place_name(data["last_clicked"]["lat"], data["last_clicked"]["lng"])
        st.header(f"{location_name}")
        # st.write(GridTimeSeriesAPI.get_snow_info(lat, lon, 2023))
        # st.write(GridTimeSeriesAPI.get_snow_info(lat, lon, 2022))
    import time

    list_of_years = []
    if lat is not None:
        with st.status("Henter historiske snøberegninger fra NVE"):
            for year in range(2020,2023).__reversed__():
                st.write(f"Henter data for {year}")
                list_of_years.append(GridTimeSeriesAPI.get_snow_info(lat,lon,year))


        for year in list_of_years:
            st.write(year.date, year.snow_level())


    # write_trees({"ost":1})

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
        i = 2023
        for col in cols:
            with col:
                st.image(f"Graphics/SNOW_{random.randint(0,2)}.png", caption=i)
                # st.markdown(
                #     f"<div style='text-align: center; padding-top: 0px;'>{years_list[0][0]}</div>",
                #     unsafe_allow_html=True
                # )
            i -= 1
    # graphics = {
    #     0: "SNOW_0"
    # }




if __name__ == "__main__":
    wrapper_page()