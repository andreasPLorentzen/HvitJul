import streamlit as st
import datetime
import folium
import pandas as pd

from streamlit_folium import st_folium
from src.gts_api import GridTimeSeriesAPI
from src.svg_img import image_generation
from src.arcgis_online_functions import add_point_to_feature_layer, get_number_of_responses
from src.stedsnavn_api import get_place_name_as_markdown

# MAP settings
INPUT_MAP_CENTER = [60.0, 10.0]
INPUT_MAP_WIDTH = 750
INPUT_MAP_HEIGHT = 400
INPUT_MAP_ZOOM = 8

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
    now = datetime.datetime.now()
    if now.month > 11 and now.day > 23: 
        max_year = int(now.year) + 1 # We include this year if it is at xmas or later
    else:
        max_year = int(now.year) # If it is before xmas, then we do not include this year


    st.markdown(
        "<p>Etter vi så en grafikk som viste om det var en hvit jul i New York, begynte vi å diskutere på hvor ofte det egentlig var en hvit jul i Oslo? eller Bergen?</p>"
        "<p>Vi ble ikke helt enige og siden vi strengt talt ikke hadde bedre ting å gjøre mellom turer på ski og julemat, så lagde vi denne websiden som lar deg velge et sted i Norge og få svaret selv.</p>"
        "<p>Når du trykker i kartet, starter applikasjonen å hente data om snøforhold fra NVE og sjekker hvordan var snøforholdene akkurat der. Du kan selv velge hvor langt tilbake i tid du ønsker å se ved å bruke skyveknappen nedenfor, men vi anbefaler å starte med kun 14 år, da det tar litt tid å hente inn data.</p>"
        f"<p>Denne appen har hittil svart på {get_number_of_responses()} spørsmål.</p>", unsafe_allow_html=True)


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
                                     options=[y for y in range(1957, max_year).__reversed__()],
                                     value=max_year - 14)

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
            for year in range(earliest_year, max_year).__reversed__():
                year_data = GridTimeSeriesAPI.get_snow_info(lat, lon, year)
                if year_data.success == False:
                    st.write(f"Feil med data for {year}")
                else:
                    st.write(f"Hentet data for {year}")
                list_of_years.append(year_data)
            st.write("Ferdig. La det snø!")

        st.snow()
        image = image_generation(list_of_years, "Var det snø på juleaften?", f"{name}, {coords}")
        st.image(image.result_image, output_format="PNG")

        # reporting back
        add_point_to_feature_layer(lat, lon, latest_year=max_year, earliest_year=earliest_year, place_name=name)

        st.markdown(
            "<p>Den enkleste måten å dele bildet over er å høyreklikke og kopiere og lime det inn i Facebook, Twitter, eller kanskje i en presentasjon på jobben for å avslutte en diskusjon dere har? </p>",
            unsafe_allow_html=True)

        st.markdown(
            "<br><br><br><p>Vil du heller se det som en tabell? Kanskje laste ned dataen som en CSV? <br> I såfall er det bare å trykk på knappen under: </p>",
            unsafe_allow_html=True)

        with st.expander(label="Se som tabell",expanded=False):
            # testing some data visualization:
            year_data = []
            bar_chart_data = []
            for year_obj in list_of_years:
                    year_data.append(year_obj.as_dict())
                    bar_chart_data.append({"År":year_obj.date.year, "Snødybde i cm":year_obj.sd})

            df = pd.DataFrame(year_data)

            st.subheader("I tabulær form:")
            st.dataframe(df, column_config={
                "name": "Var det snø på juleaften?",
                "date": st.column_config.DatetimeColumn(
                    "År",
                    format="YYYY",
                    help="År i runder rundt solen",
                ),
                "sd": st.column_config.NumberColumn(
                    "Snødybde",
                    help="Snøybde i cm",
                ),
                "tm": None,
                # "tm": st.column_config.NumberColumn(
                #     "Temperatur",
                #     help="Temperatur i grader celsius",
                # ),
                "fsw": None,
                "fsw7d": None,
                "latitude": None,
                "longitude": None,
                "lwc": None,
                "qsw": None,
                "sdfsw": None,
                "success": None,
                "swe": None,
                "swechange7d": None,
                "age": None

                },
            hide_index=True, use_container_width=True)



            bar_df = pd.DataFrame(bar_chart_data)
            # st.write(bar_df)

            st.write("Kanskje du også ønsker å se det som et søylediagram?")
            st.bar_chart(bar_df, x="År", y="Snødybde i cm")

def more_info():
    '''
    just writes some more info
    :return:
    '''
    st.subheader("Om prosjektet")
    st.markdown("<p>Denne løsningen var et hobbyprosjekt i jula 2023 av Andreas P. Lorentzen og Johannes P. Lorentzen som startet i en diskusjon og endte med implementasjon. Vi håper at du og dere liker løsningen, og at det kanskje hjelper med å løse en diskusjon hos dere også.</p> "
                "<p>Løsningen benytter NVE sin API for xgeo.no, som gir data om beregnet snødybde for et gitt punkt. Dette gjorde det enkelt for oss, men er ikke like presist som å bruke målinger fra målestasjoner. API-et leverer data tilbake til 1957, som derfor er satt som tidligste år. Vi bruker Kartverket sin stedsnavn-API for å hente stedsnavn.</p>"
                "<p>Alt er implementert i Python ved bruk av pakken streamlit. Bruker du Python, så anbefaler vi å prøve den ut. Det er derimot noen svakheter med systemet. Spesielt en vi ikke har klart å løse med en treg markør i kartet. Hvis du vil titte på kildekoden ligger den tilgjengelig på GitHub.</p>"
                "<p>Hvis du ønsker å ta kontakt, gjør det gjerne gjennom LinkedIn.</p>"
                "<p>Andreas: <a href='https://www.linkedin.com/in/andreas-p-lorentzen/'>https://www.linkedin.com/in/andreas-p-lorentzen</a></p>"
                "<p>Johannes: <a href='https://www.linkedin.com/in/pippidis/'>https://www.linkedin.com/in/pippidis</a></p>"
                "<p>God jul<br>PS: Hvis du er en grafisk designer og vil gjøre grafikken enda bedre, så si ifra :)</p>",
                unsafe_allow_html=True)



if __name__ == "__main__":
    wrapper_page()
