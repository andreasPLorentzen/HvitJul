import datetime

import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
from src.gts_api import GridTimeSeriesAPI
from src.svg_img import image_generation
import requests

# MAP settings
INPUT_MAP_CENTER = [60.0, 10.0]
INPUT_MAP_WIDTH = 750
INPUT_MAP_HEIGHT = 400
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
                                     "skrivemåte": "Stedsnavn ikke funnet",
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

    return ("Stedsnavn ikke funnet", "", (lat,long))

def get_place_name_as_markdown(lat,long) -> str:
    '''
    Returns a markdown in html
    :param lat:
    :param long:
    :return:
    '''
    navn,distance,coords = get_place_name(lat,long)
    coords = f"{round(coords[1],2)}° øst, {round(coords[0],2)}° nord"

    html=f'<p style="font-size: 2em; font-weight: bold; margin-right: 10px; display: inline;">{navn}</p>'\
         f'<p style="font-size: 1.2em; font-weight: italic; margin-left: 10px; display: inline;">{distance}</p>'\
         f'<br/><p style="font-size: 1em; font-weight: italic; display: inline;">{coords}</p>'


    return html, str(navn), str(distance), coords

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
    st.set_page_config(page_title="Var det en hvit jul?", page_icon="./Graphics/SNOW_1.png")
    st.title("Var det en hvit jul?")
    main, about = st.tabs(["Var det en hvit jul?", "Om prosjektet"])
    with main:
        main_page()

    with about:
        more_info()


def main_page():
    lat = None
    lon = None

    # defining years to show from default
    this_year = int(datetime.datetime.now().year) + 1


    st.markdown(
        "<p>Etter vi så en grafikk som viste om det var en hvit jul i New York, begynte vi å diskutere på hvor ofte det egentlig var en hvit jul i Oslo? eller Bergen? Vi ble ikke helt enige og siden vi strengt talt ikke hadde bedre ting å gjøre mellom turer på ski og julemat, så lagde vi denne websiden som lar deg velge et sted i Norge og få svaret selv.</p>"
        "<p>Siden vi strengt talt hadde bedre ting å gjøre, så lagde vi denne websiden som lar deg velge et sted i Norge og få svaret selv.</p>"
        "<p>Når du trykker i kartet, starter applikasjonen å hente data om snøforhold fra NVE og sjekker hvordan var snøforholdene akkurat der.</p>", unsafe_allow_html=True)
    st.subheader("Trykk i kartet for å se hvor mye snø det har vært i jula")

    # setting state
    if "markers" not in st.session_state:
        st.session_state["markers"] = []

    # defining map
    m = folium.Map(location=INPUT_MAP_CENTER, zoom_start=INPUT_MAP_ZOOM, export=False, )
    fg = folium.FeatureGroup(name="Markers")

    # adding markers
    for marker in st.session_state["markers"]:
        fg.add_child(marker)

    # drawing map
    data = st_folium(m, height=INPUT_MAP_HEIGHT, width=INPUT_MAP_WIDTH, key="new", feature_group_to_add=fg)

    earliest_year = st.select_slider("Hvor langt tilbake i tid vil du se?",
                                     options=[y for y in range(1972, this_year).__reversed__()],
                                     value=this_year - 14)

    if data["last_clicked"] is not None:
        lat = data["last_clicked"]["lat"]
        lon = data["last_clicked"]["lng"]
        marker = folium.Marker([lat, lon])
        st.session_state["markers"] = [marker]

        # update marker in map
        markdown, name, distance, coords = get_place_name_as_markdown(lat, lon)
        st.markdown(markdown, unsafe_allow_html=True)


    list_of_years = []
    if lat is not None:
        with st.status("Henter historiske snøberegninger fra NVE"):
            marker = folium.Marker([lat, lon])
            st.session_state["markers"] = [marker]
            for year in range(earliest_year, this_year).__reversed__():
                year_data = GridTimeSeriesAPI.get_snow_info(lat, lon, year)
                if year_data.success == False:
                    st.write(f"Feil med data for {year}")
                else:
                    st.write(f"Hentet data for {year}")
                list_of_years.append(year_data)
            st.write("Ferdig. La det snø!")

        st.snow()
        image = image_generation(list_of_years, "Var det snø på juleaften?", f"{name} {coords}")
        st.image(image.result_image, output_format="PNG")
        st.markdown(
            "<p>Den enkleste måten å dele bildet over er å høyreklikke og kopiere og lime det inn i Facebook, Twitter, eller kanskje i en presentasjon på jobben for å avslutte en diskusjon dere har? </p>",
            unsafe_allow_html=True)
        st.markdown(
            "<p>Vil du gå enda lengere tilbake? Trykk under for å sjekke de siste 50 årene (dette tar litt lengere tid) </p>",
            unsafe_allow_html=True)

        if st.button("Utvid til 50 år"):
            earliest_year = this_year - 50
            st.write(earliest_year)


def more_info():
    '''
    just writes some more info
    :return:
    '''
    # with st.expander("Les mer om prosjektet", expanded=False):
    st.subheader("Om prosjektet")
    st.markdown("<p>Denne løsningen var et hobbyprosjekt i jula 2023 av Andreas P. Lorentzen og Johannes P. Lorentzen som startet i en diskusjon og endte med implementasjon. Vi håper at du og dere liker løsningen, og at det kanskje hjelper med å løse en diskusjon hos dere også.</p> "
                "<p>Løsningen benytter NVE sin API for xgeo.no, som gir data om beregnet snødybde for et gitt punkt. Dette gjorde det enkelt for oss, men er ikke like presist som å bruke målinger fra målestasjoner. Vi bruker Kartverket sin stedsnavn-API for å hente stedsnavn.</p>"
                "<p>Alt er implementert i Python ved bruk av pakken streamlit. Bruker du Python, så anbefaler vi å prøve den ut. Det er derimot noen svakheter med systemet. Spesielt en vi ikke har klart å løse med en treg markør i kartet. Hvis du vil titte på kildekoden ligger den tilgjengelig på GitHub.</p>"
                "<p>Hvis du ønsker å ta kontakt, gjør det gjerne gjennom LinkedIn.</p>"
                "<p>Andreas: <a href='https://www.linkedin.com/in/andreas-p-lorentzen/'>https://www.linkedin.com/in/andreas-p-lorentzen</a></p>"
                "<p>Johannes: <a https://www.linkedin.com/in/pippidis/'>https://www.linkedin.com/in/pippidis</a></p>"
                "<p>God jul<br>PS: Hvis du er en grafisk designer og vil gjøre grafikken enda bedre, så si ifra :)</p>",
                unsafe_allow_html=True)

if __name__ == "__main__":
    wrapper_page()
