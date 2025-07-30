from django.urls import path
from .views import registrazione, VistaLogin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registrazione/', registrazione, name='registrazione'),
    path('login/', VistaLogin.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='autenticazione:login'), name='logout'),
]