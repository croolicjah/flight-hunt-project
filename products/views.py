from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import CreateHuntForm
from .models import Flight, Airport, Airline
from products.fetchURL import FillDbEsky, airlines_iata
from products.scrap_flights import ScrapFlightUrl


def proba(request):
    return False

# fulfill Airports class model
class  FiLlAirports(View):
    def get(self, request):
        city = Airport()
        a = FillDbEsky('https://www2.esky.pl/api/v1.0/deals.json').cities()
        for i in set(a):
            print(i)
            city.airport_name = i[0]
            city.airport_code = i[1]
            city.city_name =  i[2]
            city.city_code = i[3]
            city.city_name_form = i[4]
            city.country_name = i[5]
            city.country_code = i[6]
            city.country_name_form = i[7]
            city.continent_code = i[8]
            city.save()


        return render(request, 'products/home.html')


# fill db with codes IATA
class AirlineIataFillDb(View):
    def get(self, request):
        airlines = Airline()
        for i in airlines_iata:
            airlines.airline_code = i
            airlines.airline_name = airlines_iata[i][0]
            # print(i,airlines_iata[i][0])
            airlines.save()
        return render(request, 'products/home.html')



class Home(View):
    def get(self, request):

        return render(request, 'products/home.html')


class CreateFlight(View):

    def get(self, request):
        forms = CreateHuntForm()
        return render(request, 'products/create.html', {'forms': forms})

    def post(self, request, *args, **kwargs):
        hunt = Flight()
        form = CreateHuntForm(request.POST, request.FILES)

        if form.is_valid():
            hunt.hunter = request.user
            hunt.image_load = form.cleaned_data['image_load']
            hunt.flight_url = form.cleaned_data['flight_url']
            hunt.title = form.cleaned_data['title']
            hunt.body = form.cleaned_data['body']
            # hunt.departure_airport = ""
            # hunt.arrival_airport = ""
            hunt.airline = form.cleaned_data['airline']
            hunt.price_amount = form.cleaned_data['price_amount']
            # hunt.flightType = ""
            hunt.depart_on = form.cleaned_data['depart_on']
            hunt.arrive_on = form.cleaned_data['arrive_on']
            hunt.save()
            return redirect('/products/' + str(hunt.id))

        return render(request, 'products/create.html')


class DetailedFlight(View):

    def get(self, request, flight_id):
        flight = get_object_or_404(Flight, pk=flight_id)
        return render(request, 'products/detail.html', {'flight': flight})

    # def post(self, request, *args, **kwargs):
    #     hunt = Flight()
    #     form = CreateHuntForm(request.POST, request.FILES)
    #
    #     if form.is_valid():
    #         hunt.hunter = request.user
    #         hunt.image_load = form.cleaned_data['image_load']
    #         hunt.flight_url = form.cleaned_data['flight_url']
    #         hunt.title = form.cleaned_data['title']
    #         hunt.body = form.cleaned_data['body']
    #         # hunt.departure_airport = ""
    #         # hunt.arrival_airport = ""
    #         hunt.airline = form.cleaned_data['airline']
    #         hunt.price_amount = form.cleaned_data['price_amount']
    #         # hunt.flightType = ""
    #         hunt.depart_on = form.cleaned_data['depart_on']
    #         hunt.arrive_on = form.cleaned_data['arrive_on']
    #         hunt.save()
    #         return redirect('home')
    #
    #     return render(request, 'products/create.html')

class ScrapyFlight(View):

    # def get(self, request, flight_id):
    #     flight = get_object_or_404(Flight, pk=flight_id)
    #     return render(request, 'products/detail.html', {'flight': flight})

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax and self.request.POST:
            url = self.request.POST['param']


            data = ScrapFlightUrl(url)
            print(data.flight)
            instance = Flight()
            instance.departure_airport = data.flight[1][2]
            ser_instance = serializers.serialize('json', [instance, ])
        # send to client side.
        return JsonResponse({"instance": ser_instance}, status=200)
