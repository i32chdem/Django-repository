from django.db import models
from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here

# Un destino es un lugar al que se puede viajar, pero sin incluir los datos respecto al viaje, como precio, etc...
class Destino(models.Model):
	lugar = models.CharField(max_length=100)
	descripcion = models.TextField()
	distancia = models.IntegerField()
	
	def __unicode__(self):
        	return self.lugar

#cada viaje incluye un unico destino, pero cada destino puedes estar en varios viajes
class Viaje(models.Model):
	destino= models.ForeignKey(Destino, null=True, default=None)
	dias = models.IntegerField()
	coste = models.IntegerField()
	desplazamiento = models.CharField(max_length=100)
	def __unicode__(self):
        	return self.destino.lugar

class Ruta(models.Model):
	nombre= models.CharField(max_length=100)
	viajes= models.ManyToManyField(Viaje,null=True, default=None)
	duracion= models.IntegerField()
	precio= models.IntegerField()
	def __unicode__(self):
		return self.nombre
