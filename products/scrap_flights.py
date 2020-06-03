import numpy as np
import csv
import json
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class ScrapFlightUrl:

    def __init__(self, link):
        self.link = link
        # recognizing fetching method by operator/OTA
        if 'ryanair' in self.link:
            self.flight = self.get_ryan()
        elif 'wizzair' in self.link:
            self.flight = self.get_wizz()
        elif 'skyscanner' in self.link:
            self.flight = self.get_skyscan()


    def get_ryan(self):
        # setting up browser with minimals
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1200x600')
        driver = webdriver.Chrome(options=options)

        # fetching url
        driver.get(self.link)
        assert "Ryan" in driver.title

        timeout = 2

        # scraping only the one class with all flights data
        try:
            # wait for card-wraper loaded
            WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "card-wrapper")))

            # find_elements_by_xpath returns an array of selenium objects.
            outbound_flight =  driver.find_elements(By.CLASS_NAME, 'card-wrapper')

            # use list comprehension to not the selenium objects.
            self.flight =[x.text.split('\n') for x in outbound_flight if 'yprzedan' not in x.text]

            # print out all values. only for testing
            # [print(i) for i in flight]
            driver.quit()

        except TimeoutException:
            self.flight = 'Timed out waiting for page to load'
            driver.quit()
        return self.flight


    def get_ryan_not_selenium(self):
        # slicing url to fetch data for json payload. returns:
        # ['adults=1', 'teens=0', 'children=0', 'infants=0', 'dateOut=2020-07-05', 'dateIn=2020-07-08', 'originIata=KRK',
        #  'destinationIata=STN', 'isConnectedFlight=false', 'isReturn=true', 'discount=0', 'tpAdults=1', 'tpTeens=0',
        #  'tpChildren=0', 'tpInfants=0', 'tpStartDate=2020-07-05', 'tpEndDate=2020-07-08', 'tpOriginIata=KRK',
        #  'tpDestinationIata=STN', 'tpIsConnectedFlight=false', 'tpIsReturn=true', 'tpDiscount=0', 'TimeOut=06:55',
        #  'TimeIn=08:45', 'FareKeyOut=0~H~%20~FR~HZ8LOW~BND8~~0~2~~X', 'FareKeyIn=0~N~%20~FR~NDARREN~111C~~0~2~~X',
        #  'flightKeyOut=FR~2433~%20~~KRK~07%2F05%2F2020%2006:55~STN~07%2F05%2F2020%2008:20~~',
        #  'flightKeyIn=FR~2432~%20~~STN~07%2F08%2F2020%2008:45~KRK~07%2F08%2F2020%2012:00~~']

        ryan_sliced = link[(link.find('?') + 1):].split('&')
        # dictionaary is going to be more useful then list
        ryan_data = {slice[:slice.find('=')]:slice[(slice.find('=') + 1):] for slice in ryan_sliced}

        ryan_payload = {
            "ADT": ryan_data['adults'], "CHD": ryan_data['children'], "DateOut": ryan_data['dateOut'],
            "Destination": ryan_data['children'], "Disc": ryan_data['children'], "INF": ryan_data['infants'],
         "Origin": ryan_data['children'], "TEEN": ryan_data['teens'], "FlexDaysOut": "4", "ToUs": "AGREED", "IncludeConnectingFlights":  ryan_data['tpIsConnectedFlight'],
         "RoundTrip": ryan_data['children']}

    # Wizzair API handling
    def get_wizz(self):
        # set up headers and json payload

        headers = {
            'Host': 'be.wizzair.com', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://wizzair.com/pl-pl/', 'Content-Type': 'application/json;charset=utf-8', 'Content-Length': '280',
            'Origin': 'https://wizzair.com', 'Connection': 'keep-alive', 'TE': 'Trailers', 'Pragma': 'no-cache',
            'Cache-Control': 'no-cache', 'X-Requested-With': 'XMLHttpRequest'
        }

        params = {
            'isFlightChange': False, 'isSeniorOrStudent': False,
            'flightList': [
                {'departureStation': 'WAW', 'arrivalStation': 'SPU', 'departureDate': '2020-07-30'},
                {'departureStation': 'SPU', 'arrivalStation': 'WAW', 'departureDate': '2020-08-08'}
            ],
            'adultCount': 1, 'childCount': 0, 'infantCount': 0, 'wdc': False
        }
        # getting API version
        api_v = requests.get('https://wizzair.com/buildnumber')

        # slicing for the number
        api_version = api_v.text[api_v.text.rfind('https://be.wizzair.com/'):api_v.text.rfind(' ')]

        # striking wizzair API. response has got all needed data
        link = requests.post(api_version + '/Api/search/search', data=json.dumps(params), headers=headers)

        # second shot to API to fetch pricechart. needed for checking

        headers2 = {
            'Host': 'be.wizzair.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://wizzair.com/pl-pl/',
            'Content-Type': 'application/json;charset=utf-8',
            'X-RequestVerificationToken': 'cfad26e9cc264f4a98dea95158650a3c',
            'Content-Length': '235',
            'Origin': 'https://wizzair.com',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'TE': 'Trailers',
        }

        params2 = {'adultCount': 1, 'childCount': 0, 'dayInterval': 3, 'flightList': [{'arrivalStation': 'HRK', 'date': '2020-06-06', 'departureStation': 'KTW'}, {'arrivalStation': 'KTW', 'date': '2020-06-09', 'departureStation': 'HRK'}], 'isRescueFare': False, 'wdc': False}
        link2 = requests.post('https://be.wizzair.com/10.20.0/Api/asset/farechart', data=json.dumps(params2), headers=headers2)

        return self.flight

    def get_skyscan(self):
        # setting up browser with minimals
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1200x600')
        options.page_load_strategy = 'eager'
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)

        # fetching url
        driver.get(self.link)
        assert "Sky" in driver.title

        timeout = 10

        # scraping only the one class with all flights data
        try:
            # wait for card-wraper loaded
            # .until(EC.visibility_of_element_located((By.CLASS_NAME, "DetailsPanelContent_item__1p5EV DetailsPanelContent_left__2E3T8")))

            # find_elements_by_xpath returns an array of selenium objects.
            prices = [price.text for price in WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "price")))]
            # [print(i) for i in outbound_flight]
            # use list comprehension to not the selenium objects.
            # flight = [x.text.split('\n') for x in outbound_flight if 'yprzedan' not in x.text]
            print(prices)
            # print out all values. only for testing
            # [print(i) for i in flight]
            driver.quit()

        except TimeoutException:
            print("Timed out waiting for page to load")
            flight = 'Timed out waiting for page to load'
            driver.quit()
        return None

if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    url1 = 'http://subway.co.kr/storeSearch?page='
    url2 = '&rgn1Nm=&rgn2Nm=#storeList'

    addresses = []
    names = []
    phones = []

    for i in range(1, 42):
        driver.get(url1 + str(i) + url2)
        # change here. you have got
        lst = driver.find_elements_by_xpath('/html/body/div/div[2]/div[2]/div[3]/div/div/div[1]/table/tbody/tr')

        for row in lst:
            ####### THIS IS WHERE IT NEEDS AN ANSWER ################################################
            r = row.text.split('\n')
            addresses.append(r[2])
            names.append(r[1])
            phones.append(r[4])
    ######################################################################################
    stores = [{
        'address': props[0],
        'name': props[1],
        'phone': props[2]
    } for props in zip(addresses, names, phones)]

    with open('stores.csv', 'w') as csvfile:
        csvout = csv.DictWriter(csvfile, ['address', 'name', 'phone'])
        csvout.writeheader()
        csvout.writerows(stores)



headers = {
            'Host': 'be.wizzair.com', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://wizzair.com/pl-pl/', 'Content-Type': 'application/json;charset=utf-8', 'Content-Length': '280',
            'Origin': 'https://wizzair.com', 'Connection': 'keep-alive', 'TE': 'Trailers', 'Pragma': 'no-cache',
            'Cache-Control': 'no-cache', 'X-Requested-With': 'XMLHttpRequest'
        }

params = {
    'isFlightChange': False, 'isSeniorOrStudent': False,
    'flightList': [
        {'departureStation': 'WAW', 'arrivalStation': 'SPU', 'departureDate': '2020-07-30'},
        {'departureStation': 'SPU', 'arrivalStation': 'WAW', 'departureDate': '2020-08-08'}
    ],
    'adultCount': 1, 'childCount': 0, 'infantCount': 0, 'wdc': False
}

searchParams = {
    "inboundDate":"2020-08-27", "outboundDate":"2020-08-21","tripType":"return",
    "preferDirects":False,
    "legs":[
        {
            "originId":"WAW","originCityId":"WARS","originCountryId":"PL",
            "originName":"Warszawa Chopina","originType":"Airport","destinationId":"KHAR",
            "destinationCityId":"KHAR","destinationCountryId":"UA","destinationName":"Charków",
            "destinationType":"City","date":"2020-08-21"
        },
        {
            "originId":"KHAR","originCityId":"KHAR","originCountryId":"UA","originName":"Charków",
            "originType":"City","destinationId":"WAW","destinationCityId":"WARS",
            "destinationCountryId":"PL","destinationName":"Warszawa Chopina",
            "destinationType":"Airport","date":"2020-08-27"
        }
    ],
    "cabinClass":"economy",
    "origin":{
        "id":"WAW","airportId":"WAW","name":"Warszawa Chopina","cityId":"WARS",
        "cityName":"Warszawa","countryId":"PL","type":"Airport",
        "centroidCoordinates":[20.966667,52.166667]
    },
    "originId":"WAW","originName":"Warszawa Chopina","originType":"Airport",
    "originCityId":"WARS","originIataCode":"WAW","originCityName":"Warszawa",
    "destination":{
        "id":"KHAR","name":"Charków","cityId":"KHAR","cityName":"Charków","countryId":"UA",
        "type":"City","centroidCoordinates":[36.2500008494,50.0000050256]
    },
    "destinationId":"KHAR","destinationName":"Charków","destinationType":"City",
    "destinationCityId":"KHAR","destinationIataCode":"KHAR","destinationCityName":"Charków",
    "adultsV2":2,"originalAdults":2,"outboundAlts":False,"inboundAlts":False
}