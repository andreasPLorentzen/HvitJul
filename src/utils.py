
import math
import pyproj
def polygon_from_point(lat:float, long:float, radius:float, sides:int=6) -> str:
    """
    Generate a WKT polygon for a circle, hexagon, or heptagon.

    :param lat: latitude
    :param long: longitude
    :param radius: radius of the polygon in meters
    :param sides: number of sides (6 for hexagon, 7 for heptagon)
    :return: string with WKT polygon
    """

    if sides not in [6, 7]:
        raise ValueError("Number of sides must be 6 (hexagon) or 7 (heptagon).")

    # Function to calculate the coordinates of a point on a circle
    def calculate_point(lat, long, radius, angle_deg):
        angle_rad = math.radians(angle_deg)
        lat_new = lat + (radius / 111.32) * math.cos(angle_rad)
        long_new = long + (radius / (111.32 * math.cos(math.radians(lat)))) * math.sin(angle_rad)
        return round(lat_new,3), round(long_new,3)

    # Generate polygon points
    polygon_points = []
    for i in range(sides):
        angle = 360 * i / sides
        point = calculate_point(lat, long, radius, angle)
        polygon_points.append(point)

    # Add the first point to close the polygon
    polygon_points.append(polygon_points[0])

    # Format WKT polygon
    wkt_polygon = "POLYGON((" + ",".join([f"{point[1]} {point[0]}" for point in polygon_points]) + "))"

    return wkt_polygon


import warnings
warnings.simplefilter(action='ignore') # Needed as the proj give a futurewarning
def convert_coordinates(lat:float, lon:float, epsg_code:int=32633) -> (float, float):
    """
    Convert latitude and longitude to UTM or another coordinate system using an EPSG code.

    :param lat: Latitude
    :param lon: Longitude
    :param epsg_code: EPSG code for the target coordinate system
    :return: UTM or target coordinate system coordinates

    epsg_code_utm_33N = 32633 #https://epsg.io/32633
    """
    # Define the projection for WGS 84 (latitude and longitude)
    wgs84 = pyproj.Proj(init='epsg:4326')

    # Define the projection for the target coordinate system
    target_proj = pyproj.Proj(init=f'epsg:{epsg_code}')

    # Convert latitude and longitude to the target coordinate system
    x, y = pyproj.transform(wgs84, target_proj, lon, lat)

    return x, y


if __name__ == "__main__":
    print(convert_coordinates(59.9,10.67))