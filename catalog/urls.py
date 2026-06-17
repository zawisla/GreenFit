from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.plant_list, name="list"),
    path("<int:pk>/", views.plant_detail, name="detail"),
]
