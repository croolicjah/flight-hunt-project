# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
# from scrapy_djangoitem import DjangoItem
from products.models import Flight

# class FlightItem(DjangoItem):
#     django_model = Flight

class TravelScrapItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    quote = scrapy.Field()

