from django.urls import path

from . import views

app_name = "selector"

urlpatterns = [
    path("", views.home, name="home"),
    path("select/", views.select, name="select"),
    path("result/<int:pk>/", views.result, name="result"),
    path("statistics/", views.statistics, name="statistics"),
    path("history/", views.history, name="history"),
    path("api/weather/", views.weather_api, name="weather_api"),
]
