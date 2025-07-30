# models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email deve essere impostata')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

class Utente(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email', unique=True)
    nome = models.CharField('nome', max_length=50)
    cognome = models.CharField('cognome', max_length=100)
    ruolo = models.CharField('ruolo', max_length=50)
    appartenenza = models.CharField('appartenenza', max_length=100)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cognome', 'ruolo', 'appartenenza']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.nome} {self.cognome}"

    class Meta:
        verbose_name = 'Utente'
        verbose_name_plural = 'Utenti'
        ordering = ['nome', 'cognome'] 