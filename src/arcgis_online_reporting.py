'''
this function anonymously reports the position and the datetime.
Only to run statistics.
'''

import requests
import json
from datetime import datetime

def add_point_to_feature_layer(lat, lon, use_date_attribute=True):
    # ArcGIS Online feature layer Add Features endpoint
    add_features_url = "https://services6.arcgis.com/XQb5TfenBnLwbfWV/arcgis/rest/services/hvit_jul_response/FeatureServer/0/addFeatures"

    # Define the headers and the geometry+attributes for the feature you want to add
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Prepare the attributes, including the current time for use_date in UTC and ISO format
    attributes = {}
    if use_date_attribute:
        attributes["use_date"] = datetime.utcnow().isoformat()

    # Define the feature to be added
    # Note: 'geometry' should include the spatial reference (wkid) and the x, y coordinates for the point
    # Replace 'x' and 'y' with actual coordinates
    feature = {
        "attributes": attributes,
        "geometry": {
            "spatialReference": {"wkid": 4326},
            "x": lon,  # Replace this with the actual longitude
            "y": lat  # Replace this with the actual latitude
        }
    }

    # Make the POST request to the Add Features endpoint
    response = requests.post(add_features_url, headers=headers, data=json.dumps({
        "features": [feature],
        "f": "json"
    }))

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return response.text