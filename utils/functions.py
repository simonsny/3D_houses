import requests

import json

URL = "https://api.basisregisters.vlaanderen.be/v1/adresmatch"

def get_info_from_adress(params: dict) -> list:
    """ Function that takes in an andress in the form of params,
    sends it to an api and returns a polygon with coordinates of the house.

    :param params: parameters to give to requests get
     params = {"postcode": xxxx, "straatnaam": 'string_street', "huisnummer": xx }
    :return: Polygon of the shape of the house we want to visualize
    """
    jayson = request_json_content(URL, params)
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
    :return: List with polygon in it
    """
    jayson = request_json_content(url)
    details_url = jayson['gebouw']['detail']

    jayson_poly = request_json_content(details_url)
    poly = jayson_poly['geometriePolygoon']['polygon']['coordinates']
    return poly


def request_json_content(url: str, params=None) -> dict:
    """
    Function to make request content of an url. Shortens often used code for easier reading.
    :param url: URL to make an api call to
    :param params: Paramaters to give to the requests
    :return: json obj with content of API call
    """
    request = requests(url, params)
    content = request.content
    jayson = json.loads(content)
    return jayson
