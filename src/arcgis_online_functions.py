'''
this function anonymously reports the position and the datetime.
Only to run statistics.
'''

import requests
from datetime import datetime
import streamlit as st

def add_point_to_feature_layer(lat, lon, latest_year, earliest_year,place_name):
    # ArcGIS Online feature layer Add Features endpoint
    add_features_url = "https://services6.arcgis.com/XQb5TfenBnLwbfWV/arcgis/rest/services/hvit_jul_response/FeatureServer/0/addFeatures"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    features = [{
        "attributes": {
            "use_date": datetime.now().isoformat(),
            "latest_year": int(latest_year),
            "earliest_year": int(earliest_year),
            "place_name": str(place_name)
        },
        "geometry": {
            "spatialReference": {
                "wkid": 4326,
            },
            "x": lon,
            "y": lat,
        },
    }]


    # Make the POST request to the Add Features endpoint
    response = requests.post(url=add_features_url,
                             data={
                                "features": str(features),
                                "rollbackOnFailure": True,
                                "f": "json"
                            },
                            headers=headers
                            )

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return response.text


def get_number_of_responses() -> int:
    feature_service_url = "https://services6.arcgis.com/XQb5TfenBnLwbfWV/arcgis/rest/services/hvit_jul_response/FeatureServer/0"
    # Append '/query' to the feature service URL to perform a query operation
    query_url = f"{feature_service_url}/query"

    # Specify the parameters for the query to retrieve the count of features
    params = {
        'where': '1=1',  # A condition that selects all features
        'returnCountOnly': 'true',
        'f': 'json'  # Specify the response format as JSON
    }

    # Make a GET request to the query endpoint
    response = requests.get(query_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response and retrieve the count of features
        result = response.json()
        count = result.get('count', 0)
        return count
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}, {response.text}")
        return -1


if __name__ == "__main__":
    # print(add_point_to_feature_layer(60,10, 2023, 2011))
    print(f"Hittil er det genrerert {get_number_of_responses()} bilder gjennom denne appen.")