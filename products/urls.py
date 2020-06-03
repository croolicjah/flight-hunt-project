"""product_hunt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from products.views import Home
from .views import CreateFlight, DetailedFlight, ScrapyFlight

urlpatterns = [
    path('create/', login_required(CreateFlight.as_view()), name='create'),
    path('<int:flight_id>/', DetailedFlight.as_view(), name='detail'),
    path('scrap_flights/', ScrapyFlight.as_view(), name='scrapy_flights'),

]
