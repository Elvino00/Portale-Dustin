from django.db import models

# Create your models here.
class Device(models.Model):
    nome_azienda = models.CharField(max_length=100)
    id_servizio_azienda = models.CharField(max_length=100)
    nome_veicolo = models.CharField(max_length=100)
    id_device = models.CharField(max_length=50)
    nome_entita = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=100)
    sottogruppo = models.CharField(max_length=50)

    def __str__(self):
        return self.nome_veicolo
