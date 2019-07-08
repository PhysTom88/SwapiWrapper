import requests


class SwapiWrapper:

    SWAPI_URL = "https://swapi.co/api/"

    def __init__(self):
        self.ships = list()

    def get_all_starships(self, page=None):
        if not page:
            page = 1
        url = self.SWAPI_URL + "starships/?page={0}".format(page)
        req = requests.get(url=url)

        data = req.json()

        self.ships += data["results"]

        if data["next"]:
            self.get_all_starships(page=page + 1)
