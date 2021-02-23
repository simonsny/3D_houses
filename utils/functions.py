import requests

def request_adress_geopunt(adress: str) -> dict:
    url = "http://loc.geopunt.be/geolocation/location?"
    params = {
        'q':adress,
        'c': 1
    }
    return requests.get(url, params)