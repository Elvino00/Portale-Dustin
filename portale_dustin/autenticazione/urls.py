from django.urls import path
from . import views

app_name = 'autenticazione'

urlpatterns = [
    path('register/', views.register, name='register'),
]