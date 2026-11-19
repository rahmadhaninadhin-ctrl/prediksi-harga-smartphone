from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/prediksi/", views.api_prediksi, name="api_prediksi"),
    path("api/grafik/", views.api_grafik, name="api_grafik"),
]