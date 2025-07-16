from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registrazione completata con successo!. Ora puoi effettuare il log in.")
            return redirect('register') 
    else:
        form = UserCreationForm()
    return render(request, "autenticazione/registrazione.html" , {"form" : form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, "autenticazione/login.html" , {"form" : form})

@login_required
def home_view(request):
    return render(request, "autenticazione/home.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Logout effettuato con successo!")
    return redirect('login')