from django.db import models
from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User
from django.contrib import admin


class Destinatario (models.Model):
	nombre = models.CharField (max_length = 128)
	direccion = models.CharField (max_length = 128)
	ciudad = models.CharField (max_length = 128)
	codigo_postal = models.IntegerField ()
	def __unicode__(self):
		return (self.nombre + " con direccion en: " + self.direccion)

class Paquete (models.Model):
	contenido = models.CharField (max_length = 128)
	valor = models.IntegerField ()
	destinatario= models.ForeignKey(Destinatario, default=None)
	def __unicode__(self):
		return (self.contenido)

class Ruta (models.Model):
	nombre = models.CharField (max_length = 128)
	paquetes= models.ForeignKey(Paquete, default=None)
	def __unicode__(self):
		return (self.nombre)

