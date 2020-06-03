from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required

class Home(View):
    def get(self, request):
        #  <view logic>

        return render(request, 'products/home.html')

@login_required()
class CreateFlight():
    class Login(View):
        def get(self, request):
            #  <view logic>

            return render(request, 'products/create.html')

        def post(self, request, *args, **kwargs):

            return render(request, 'products/create.html', {'error': 'Login lub hasło są niepoprawne!!!'})