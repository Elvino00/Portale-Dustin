from django.shortcuts import render, redirect
from .forms import FormCreazioneUtente , FormAutenticazioneEmail
from django.contrib.auth.views import LoginView

def registrazione(request):
    if request.method == 'POST':
        form = FormCreazioneUtente(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = FormCreazioneUtente()
    return render(request, 'autenticazione/registrazione.html', {'form': form})

class VistaLogin(LoginView):
    form_class = FormAutenticazioneEmail
    template_name = 'autenticazione/login.html'
