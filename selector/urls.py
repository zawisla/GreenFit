from django.urls import path

from . import views

app_name = "selector"

urlpatterns = [
    path("api/weather/", views.weather_api, name="weather_api"),
]
