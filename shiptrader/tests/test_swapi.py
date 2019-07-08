from django.test import TestCase

import responses

from shiptrader.lib.swapi import SwapiWrapper
from shiptrader.tests.mock_swapi import SWAPI_NO_NEXT_RESPONSE, SWAPI_WITH_NEXT_RESPONSE


class TestSwapiWrapper(TestCase):

    @responses.activate
    def test_get_ships(self):
        responses.add(
            responses.GET, "https://swapi.co/api/starships/?page=1", json=SWAPI_WITH_NEXT_RESPONSE
        )
        responses.add(
            responses.GET, "https://swapi.co/api/starships/?page=2", json=SWAPI_NO_NEXT_RESPONSE
        )

        swapi = SwapiWrapper()
        swapi.get_all_starships()

        self.assertTrue(len(swapi.ships), 2)
