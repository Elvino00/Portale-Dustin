from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utente

class CustomUserAdmin(UserAdmin):
    # Ordine dei campi nella pagina di modifica
    fieldsets = (
        (None, {'fields': ('nome', 'cognome', 'email', 'ruolo', 'appartenenza')}),
        ('Password', {'fields': ('password',)}),  # Spostato in fondo
        ('Permessi', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Date importanti', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Ordine dei campi nella pagina di creazione
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nome', 'cognome', 'email', 'ruolo', 'appartenenza', 'password1', 'password2'),
        }),
    )
    
    # Ordine nella lista utenti
    list_display = ('nome', 'cognome', 'email', 'ruolo', 'appartenenza')
    search_fields = ('nome', 'cognome', 'email')
    ordering = ('nome', 'cognome')

admin.site.register(Utente, CustomUserAdmin)