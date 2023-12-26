'''
This file consist of unused functions and stuff that might be usefull if we want to expand.

'''

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


def placenames_options(querey):
    if len(querey) < 4:
        return [""]
    return get_x_first_place_names(querey)[0]