from django.urls import path
from . import views

urlpatterns = [
    path('' , views.home , name='home'),
    path('veicoli/<str:id_device>/' , views.dettaglio_veicolo , name = 'dettaglio_veicolo'), 
]

