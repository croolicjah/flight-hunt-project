from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Airport(models.Model):
    airport_name = models.CharField(max_length=55)
    airport_code = models.CharField(max_length=5)
    city_name = models.CharField(max_length=55)
    city_name_form = models.CharField(max_length=55)
    country_name = models.CharField(max_length=55)
    country_code =  models.CharField(max_length=10)
    country_name_form = models.CharField(max_length=55)


class Airline(models.Model):
    airline_name = models.CharField(max_length=70)
    airline_code = models.CharField(max_length=6)


class Flight(models.Model):
    hunter = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), null=True)
    image_load = models.ImageField(upload_to='images/', null=True, blank=True)
    flight_url = models.URLField(max_length=400)
    title = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField(max_length=800, null=True, blank=True)
    departure_airport = models.CharField(max_length=15)
    arrival_airport = models.CharField(max_length=15)
    airline = models.CharField(max_length=15)

    price_amount = models.DecimalField(max_digits=10, decimal_places=2)
    flightType = models.CharField(max_length=15)

    depart_on = models.DateField(null=True, blank=True)
    arrive_on = models.DateField(null=True, blank=True)
    votes_total = models.IntegerField(default=1)
    # views = models.IntegerField()
    # scoring = models.DecimalField(max_digits=5, decimal_places=2)

    offered_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title