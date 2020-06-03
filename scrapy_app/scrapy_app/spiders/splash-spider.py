import scrapy
import scrapy_splash
from scrapy_splash import SplashRequest

class MySpider(scrapy.Spider):
    name = "jsscraper"

    start_urls = ["https://wizzair.com/pl-pl/#/booking/select-flight/GDN/LTN/2020-05-30/2020-06-28/2/0/0"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='render.html')

    def parse(self, response):
        for q in response.css("div.flight-select__flight-list"):
            quote = {'flight':'', 'quote':'',}
            quote["author"] = q.css(".flight-select__flight__line::text").extract_first()
            # quote["quote"] = q.css(".text::text").extract_first()
            yield quote


