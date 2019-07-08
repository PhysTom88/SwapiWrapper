from django.db import models
from django.utils import timezone


class Starship(models.Model):
    starship_class = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)

    length = models.CharField(max_length=20)
    hyperdrive_rating = models.CharField(max_length=20)
    cargo_capacity = models.CharField(max_length=20)

    crew = models.CharField(max_length=20)
    passengers = models.CharField(max_length=20)


class Listing(models.Model):
    name = models.CharField(max_length=255)
    ship_type = models.ForeignKey(Starship, related_name='listings')
    price = models.IntegerField()
    listed_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
