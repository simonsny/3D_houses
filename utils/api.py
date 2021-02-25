import requests

from shapely import geometry

URL = "https://api.basisregisters.vlaanderen.be/v1/adresmatch"


def get_polygon_from_adress_params(params: dict) -> list:
    """ Function that takes in an andress in the form of params,
    sends it to an api and returns a polygon with coordinates of the house.

    :param params: parameters to give to requests get
     params = {"postcode": xxxx, "straatnaam": 'string_street', "huisnummer": xx }
    :return: Polygon of the shape of the house we want to visualize
    """
    jayson = requests.get(URL, params).json()
    address_objects = jayson['adresMatches'][0]['adresseerbareObjecten']
    polygons = []
    for obj in address_objects:
        if obj['objectType'] == 'gebouweenheid':
            polygons.append(get_polygon_from_detail_url_gebouweenheid(obj['detail']))
    return polygons


def get_polygon_from_detail_url_gebouweenheid(url: str) -> list:
    """
    Function that uses an url to find building unit info, in which we find info off the buildings, using that detail
    url to find the polygon of said building.
    :param url: API url to the building unit
    :return: polygon
    """
    jayson = requests.get(url).json()
    details_url = jayson['gebouw']['detail']

    jayson_poly = requests.get(details_url).json()
    poly = jayson_poly['geometriePolygoon']['polygon']['coordinates']
    poly = geometry.Polygon(poly[0])
    return poly
