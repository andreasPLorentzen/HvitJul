'''
this function anonymously reports the position and the datetime.
Only to run statistics.
'''

import requests
import json
from datetime import datetime

def add_point_to_feature_layer(lat, lon):
    # ArcGIS Online feature layer Add Features endpoint
    add_features_url = "https://services6.arcgis.com/XQb5TfenBnLwbfWV/arcgis/rest/services/hvit_jul_response/FeatureServer/0/addFeatures"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    features = [{
        "attributes": {
            "use_date": datetime.now().isoformat()
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



if __name__ == "__main__":
    print(add_point_to_feature_layer(60,10))