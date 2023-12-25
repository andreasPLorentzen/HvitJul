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



    # data = st_folium(f_m, height=INPUT_MAP_HEIGHT, width=INPUT_MAP_WIDTH,  feature_group_to_add=fg, key="new")
    data = st_folium(m, height=300, width=750)

    # data =  st_folium(m)
    # # if data["last_clicked"] is not None:
    if data.get("last_clicked"):
        marker = folium.Marker([data["last_clicked"]["lat"], data["last_clicked"]["lng"]])
        st.session_state["markers"] = [marker]


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

def get_place_name(lat,long) -> (str, str, (float, float)):
    # Using kartverkets API
    base_url = "https://api.kartverket.no/stedsnavn/v1/punkt"
    params = {
        "nord": lat,
        "ost": long,
        "koordsys": 4258,
        "radius": 300,
        "fuzzy": "true",
        "utkoordsys": "4258",
        "treffPerSide": "10",
        "side": "1"
    }

    # getting response from API inside search radius. the radius doubles every try
    while True:

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            if len(response.json()["navn"]) >= 1:
                data = response.json()["navn"]
                break
        params["radius"] *= 2
        # st.write(params["radius"], "meter...")

        if params["radius"] > 10000:
            data =  [
                        {
                            "meterFraPunkt": 0,
                            "navneobjekttype": "Adressenavn",
                            "representasjonspunkt": {
                                "koordsys": 4258,
                                "nord": long,
                                "øst": lat,
                               },
                            "stedsnavn": [
                                 {
                                     "navnestatus": "hovednavn",
                                     "skrivemåte": "Stedsnvan ikke funnet",
                                     "skrivemåtestatus":"vedtatt",
                                     "språk": "Norsk",
                                     "stedsnavnnummer": 1
                                },
                            ],
                            "stedsnummer": 987210,
                            "stedstatus": "aktiv",
                    },
             ]

            break

    if response.status_code == 200:
        try:
            data = response.json()["navn"]
            closest_name = data[0]

            # Finds closest name object
            for name_obj in data:
                if name_obj["meterFraPunkt"] < closest_name["meterFraPunkt"]:
                    closest_name = name_obj

            return (closest_name["stedsnavn"][0]["skrivemåte"], str(closest_name["meterFraPunkt"]) + " meter fra valgt punkt", (closest_name["representasjonspunkt"]["nord"], closest_name["representasjonspunkt"]["øst"]))
        except:
            pass

    return ("Stedsnvan ikke funnet", "", (lat,long))

def get_place_name_as_markdown(lat,long) -> str:
    '''
    Returns a markdown in html
    :param lat:
    :param long:
    :return:
    '''
    navn,distance,coords = get_place_name(lat,long)

    html=f'<p style="font-size: 2em; font-weight: bold; margin-right: 10px; display: inline;">{navn}</p>'\
         f'<p style="font-size: 1.2em; font-weight: italic; margin-left: 10px; display: inline;">{distance}</p>'\
         f'<br/><p style="font-size: 1em; font-weight: italic; display: inline;">{round(coords[1],2)}° øst, {round(coords[0],2)}° nord</p>'


    return html

def placenames_options(querey):
    if len(querey) < 4:
        return [""]
    return get_x_first_place_names(querey)[0]


def place_querey():
    pass

    # place_query = st.text_input("Enter a place name", "")
    # if place_query:
    #     # place_names = get_place_names(place_query)
    #     # st.write(place_names)
    #     first_10_place_names, place_names = get_x_first_place_names(place_query, 10)
    #     # st.write(first_10_place_names)
    #     if 'navn' in place_names:
    #         # options = [place['navn'] for place in place_names['navn']]
    #         options = first_10_place_names
    #         st.selectbox("Select a place", options)
    #     else:
    #         st.warning("No places found for your query.")

    # test = "Tynset"
    # options = placenames_options(test)
    # test = st.selectbox("Søk på stedsnavn", placenames_options(test))
    # st.write(test)

def wrapper_page():
    # st.set_page_config(layout="wide")
    lat = None
    lon = None

    st.title("Hvor hvit er egentlig jula?")
    st.markdown("Etter vi så en grafikk som viste om det var en hvit jul i New York, begynte vi å lure på hvor ofte var det egentlig en hvit jul i Oslo? eller Bergen?"
            "Siden vi strengt talt hadde bedre ting å gjøre, så lagde vi denne websiden som lar deg velge et sted i Norge og få svaret selv.<br/><br/>"
            "Løsningen baserer seg på Kartverket sitt Stedsnvan API og NVE sitt GridTimeSeries data (GTS) API. Sistnevnte gir beregnet snødybde, nysnø og alt annet funnet i www.xgeo.no",unsafe_allow_html=True)

    #setting state
    if "markers" not in st.session_state:
        st.session_state["markers"] = []

    # defining map
    m = folium.Map(location=INPUT_MAP_CENTER, zoom_start=INPUT_MAP_ZOOM, export=False, )
    fg = folium.FeatureGroup(name="Markers")


    # adding markers
    for marker in st.session_state["markers"]:
        fg.add_child(marker)

    # drawing map
    data = st_folium(m, height=300, width=750, key="new", feature_group_to_add=fg)

    # if data.get("last_clicked"):
    #     marker = folium.Marker([data["last_clicked"]["lat"], data["last_clicked"]["lng"]])
    #     st.session_state["markers"] = [marker]



    # data = draw_trip_in_map()
    # st.write(data)
    # st.write(data["last_clicked"])

    if data["last_clicked"] is not None:
        marker = folium.Marker([lat, lon])
        st.session_state["markers"] = [marker]
        lat = data["last_clicked"]["lat"]
        lon = data["last_clicked"]["lng"]

        # update marker in map
        st.markdown(get_place_name_as_markdown(lat,lon),unsafe_allow_html=True)


    import time

    list_of_years = []
    if lat is not None:
        with st.status("Henter historiske snøberegninger fra NVE"):
            marker = folium.Marker([lat, lon])
            st.session_state["markers"] = [marker]
            for year in range(2020,2024).__reversed__():
                year_data = GridTimeSeriesAPI.get_snow_info(lat,lon,year)
                if year_data.success == False:
                    st.write(f"Feil med data for {year}")
                else:
                    st.write(f"Hentet data for {year}")
                list_of_years.append(year_data)
            st.write("done! let it snow")
            st.snow()


        for year in list_of_years:
            st.write(year.date.year, year.snow_level(), year.sd)


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