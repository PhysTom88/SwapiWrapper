import json

from django.test import TestCase


class TestApi(TestCase):

    fixtures = ['shiptrader_ships.json']


class TestShipsView(TestApi):

    def test_get_ships(self):
        url = "/starships/ships/"
        content = self.client.get(url)
        self.assertEqual(content.status_code, 200)

        data = content.json()
        self.assertTrue(isinstance(data, list))


class TestShipListingsView(TestApi):

    fixtures = ['shiptrader_listings.json']

    def test_get_listings_ok(self):
        url = "/starships/listings/?starship_class=Starfighter"
        content = self.client.get(url)
        self.assertEqual(content.status_code, 200)

        data = content.json()
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(len(data["listings"]), 3)

    def test_price_ordering(self):
        url = "/starships/listings/?starship_class=Starfighter&sort_by=price"
        content = self.client.get(url)
        self.assertEqual(content.status_code, 200)

        data = content.json()
        self.assertTrue(data["listings"][0]["price"] < data["listings"][1]["price"])

    def test_bad_ship_class(self):
        url = "/starships/listings/?starship_class=InvalidClass"
        content = self.client.get(url)
        self.assertEqual(content.status_code, 200)

        data = content.json()
        self.assertEqual(len(data["listings"]), 0)

    def test_bad_ordering(self):
        url = "/starships/listings/?starship_class=Starfighter&sort_by=BadSort"
        content = self.client.get(url)
        self.assertEqual(content.status_code, 400)


class TestShipSaleView(TestApi):

    fixtures = ['shiptrader_listings.json']

    def test_add_listing(self):
        url = "/starships/listing/"
        content = self.client.post(url, data={
            "starship_class": "Starfighter",
            "price": "200",
            "name": "Test Ship",
            "manufacturer": "Incom Corporation"
        })

        self.assertEqual(content.status_code, 201)

        data = content.json()
        self.assertTrue(isinstance(data["listing"], dict))

    def test_bad_ship_class(self):
        url = "/starships/listing/"
        content = self.client.post(url, data={
            "starship_class": "BadClass",
            "price": "200",
            "name": "Test Ship",
            "manufacturer": "Incom Corporation"
        })

        self.assertEqual(content.status_code, 400)

    def test_bad_price(self):
        url = "/starships/listing/"
        content = self.client.post(url, data={
            "starship_class": "Starfighter",
            "price": None,
            "name": "Test Ship",
            "manufacturer": "Incom Corporation"
        })

        self.assertEqual(content.status_code, 400)

    def test_bad_name(self):
        url = "/starships/listing/"
        content = self.client.post(url, data={
            "starship_class": "Starfighter",
            "price": "200",
            "manufacturer": "Incom Corporation"
        })

        self.assertEqual(content.status_code, 400)

    def test_same_name(self):
        url = "/starships/listing/"
        content = self.client.post(url, data={
            "starship_class": "Starfighter",
            "price": "200",
            "name": "Bloody Bastard",
            "manufacturer": "Incom Corporation"
        })

        self.assertEqual(content.status_code, 400)

    def test_change_activeness_ok(self):
        url = "/starships/listing/"
        content = self.client.put(
            url,
            data=json.dumps({"name": "Bloody Bastard"}),
            content_type="application/json",
        )

        self.assertEqual(content.status_code, 200)

        data = content.json()
        self.assertTrue(isinstance(data["listing"], dict))
        self.assertFalse(data["listing"]["active"])

        active_content = self.client.put(
            url,
            data=json.dumps({"name": "Bloody Bastard"}),
            content_type="application/json",
        )

        self.assertEqual(active_content.status_code, 200)

        data = active_content.json()
        self.assertTrue(data["listing"]["active"])

    def test_activeness_bad_name(self):
        url = "/starships/listing/"
        content = self.client.put(
            url,
            data=json.dumps({"name": "Bad Name"}),
            content_type="application/json",
        )

        self.assertEqual(content.status_code, 404)