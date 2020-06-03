import scrapy

from products.scraper.items import TravelScrapItem
import json
import base64
from scrapy_splash import SplashRequest

# class WizzSpider(scrapy.Spider):
#   name = "wizzair"
#   start_urls = ["https://wizzair.com/pl-pl/#/booking/select-flight/WRO/ODS/2020-06-08/2020-06-19/1/0/0"]
#
#   # this is what start_urls does
#   # def start_requests(self):
#   #     urls = ['https://www.theodo.co.uk/team',]
#   #     for url in urls:
#   #       yield scrapy.Request(url=url, callback=self.parse)
#
#   def parse(self, response):
#       data = response.css("div.st-about-employee-pop-up")
#
#       for line in data:
#           item = FlightItem()
#           item["name"] = line.css("div.h3 h3::text").extract_first()
#           item["image"] = line.css("img.img-team-popup::attr(src)").extract_first()
#           item["fun_fact"] = line.css("div.p-small p::text").extract().pop()
#           yield item


# class WizzMsSpider(scrapy.Spider):
#     name = 'wizz-ms'
#     sitemap_urls = ['http://www.wizz.com/sitemap.xml']


class MySpider(scrapy.Spider):
    name = "jsscraper"

    start_urls = ["http://quotes.toscrape.com/js/"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='render.html')

    def parse(self, response):
        for q in response.css("div.quote"):
            quote = TravelScrapItem()
            quote["author"] = q.css(".author::text").extract_first()
            quote["quote"] = q.css(".text::text").extract_first()
            yield quote