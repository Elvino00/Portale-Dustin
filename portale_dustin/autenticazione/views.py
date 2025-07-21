from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .queries import CrateDBQueries
from django.http import  JsonResponse
import json

# Create your views here.
def register_view(request): #vista per la registrazione
    if request.method == "POST":
        form = UserRegistrationForm(request.POST) #form personalizzato creato in forms.py
        if form.is_valid(): #salvataggio nuovo utente se il form è valido. Se l'utente viene registrato con successo, si fa il redirect alla pagina di registrazione
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            messages.success(request, "Registrazione completata con successo! Ora puoi effettuare il log in.")
            return redirect('register') 
    else:
        form = UserRegistrationForm()
    return render(request, "autenticazione/registrazione.html" , {"form" : form}) #passaggio del form al template html di registrazione

def login_view(request): #vista per il login
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST) #form di autenticazione di Django
        if form.is_valid():
            user = form.get_user() #estrazione utente per passarlo alla home e mostrare messaggio di benvenuto
            login(request, user)
            return redirect('home') #redirect alla home (home.html)
    else:
        form = AuthenticationForm()
    return render(request, "autenticazione/login.html" , {"form" : form}) 

@login_required #decorator che porta alla home se il login è avvenuto con successo
def home_view(request):
    return render(request, "autenticazione/home.html")

def logout_view(request): #view di logout
    request.session.flush()
    logout(request)
    messages.success(request, "Logout effettuato con successo!")
    return redirect('login') #dopo aver effettuato il logout, ritorna alla pagina di login

def test_crate_connection(request):
    try:
        # Ottieni i dati dalla tua funzione
        data = CrateDBQueries.get_some_ecg_statistics()
        
        # Verifica manualmente la serializzabilità (solo per debug)
        try:
            json.dumps(data)  # Prova a serializzare
        except TypeError as e:
            return JsonResponse({
                'status': 'error',
                'message': f'error: {str(e)}',
                'debug': 'Verify the data contains no non-serializable objects'
            }, status=500)
        
        # Restituisci i dati come JSON
        return JsonResponse({
            'status': 'success',
            'data': data,
            'count': len(data)
        })
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)