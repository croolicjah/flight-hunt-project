from django.shortcuts import render
from django.views import View


class Home(View):
    def get(self, request):
        #  <view logic>

        return render(request, 'products/home.html')