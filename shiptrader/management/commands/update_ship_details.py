from django.core.management.base import BaseCommand

from shiptrader.lib.swapi import SwapiWrapper
from shiptrader.models import Starship


class Command(BaseCommand):

    def handle(self, *args, **options):
        swapi = SwapiWrapper()
        swapi.get_all_starships()
        for ship in swapi.ships:
            Starship.objects.update_or_create(
                starship_class=ship.get("starship_class"),
                manufacturer=ship.get("manufacturer"),
                length=ship.get("length"),
                hyperdrive_rating=ship.get("hyperdrive_rating"),
                cargo_capacity=ship.get("cargo_capacity"),
                crew=ship.get("crew"),
                passengers=ship.get("passengers")
            )

