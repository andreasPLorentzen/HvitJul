
import math
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
