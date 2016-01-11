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
		return (self.nombre + " " + self.direccion)

#un paquete tiene un destinatario, y un destinatario puede tener muchos paquetes
class Paquete (models.Model):
	destinatario= models.ForeignKey(Destinatario, null=True, default=None)
	contenido = models.CharField (max_length = 128)
	valor = models.IntegerField ()
	def __unicode__(self):
		return (self.contenido + " " + self.valor)

#una ruta esta formada por muchos paquetes y un paquete solo pertenece a una ruta
class Ruta (models.Model):
	nombre = models.CharField (max_length = 128)
	paquete= models.ForeignKey(Paquete, null=True, default=None)
	def __unicode__(self):
		return (self.nombre)

