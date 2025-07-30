from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Utente


class FormCreazioneUtente(UserCreationForm):
    class Meta:
        model = Utente
        fields = ('email', 'nome', 'cognome', 'ruolo', 'appartenenza', 'password1', 'password2')

def clean_password2(self):
    cd = self.cleaned_data
    if cd['password'] != cd['password2']:
        raise forms.ValidationError('Le password non coincidono.')
    return cd['password2']
    
def clean_email(self):
    email = self.cleaned_data.get('email')
    if Utente.objects.filter(email=email).exists():
        raise forms.ValidationError("Questa email è già registrata")

    

class FormAutenticazioneEmail(AuthenticationForm):
    username = forms.EmailField(label="Email")