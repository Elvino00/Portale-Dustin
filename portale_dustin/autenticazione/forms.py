from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Indirizzo email")
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ["username" , "email" , "password"]

    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Le password non coincidono.')
        return cd['password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email già registrata" , code='email_exists')
        return email
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rimuovi l'aiuto testo di default per non mostrarlo due volte
        self.fields['username'].help_text = ''

