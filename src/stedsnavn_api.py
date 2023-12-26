import requests

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
    # coords = f"{round(coords[1],2)}° øst, {round(coords[0],2)}° nord"
    # coords = f"({round(coords[1], 2)}°Ø, {round(coords[0], 2)}°N)"
    coords = f"{round(coords[0], 2)}°N, {round(coords[1], 2)}°Ø"

    html=f'<p style="font-size: 2em; font-weight: bold; margin-right: 10px; display: inline;">{navn}</p>'\
         f'<p style="font-size: 1.2em; font-weight: italic; margin-left: 10px; display: inline;">{distance}</p>'\
         f'<br/><p style="font-size: 1em; font-weight: italic; display: inline;">{coords}</p>'


    return html, str(navn), str(distance), coords

