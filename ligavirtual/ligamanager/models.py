from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

import sys
reload(sys)
sys.setdefaultencoding("latin-1") #para poner alfabeto castellano

class Persona(models.Model):
	nombre= models.CharField(max_length=100)
	apellidos= models.CharField(max_length=100)
	#nacimiento= models.DateField(null=True)
	def __unicode__(self):
		return self.nombre + " " + self.apellidos


class Jugador(Persona):
	posicion= models.CharField(max_length=20) #valores posibles P (Portero), D (Defensa), MC (Mediocentro) y DC (Delantero)
	precio= models.IntegerField(default=0)
	puntos= models.IntegerField(default=0)
	def __unicode__(self):
		return self.nombre + " " + self.apellidos

class Noticia(models.Model):
	contenido= models.TextField()
	autor= models.ForeignKey(settings.AUTH_USER_MODEL)
	fecha= models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.contenido

class Liga(models.Model):
	nombre= models.CharField(max_length=15) 
	password= models.CharField(max_length=20)
	mercadoFichajes= models.ManyToManyField(Jugador,default=None, null=True, blank=True, symmetrical=False) #recogera en una lista el mercado de fichajes de cada dia
	noticia=  models.ManyToManyField(Noticia, default=None, null=True)
	def __unicode__(self):
		return self.nombre

	
class Equipo(models.Model):
	nombre= models.CharField(max_length=100)
	dinero= models.IntegerField(default=20000000) #dinero inicial 20 millones 
	puntos = models.IntegerField(default=0)
	jugador=models.ManyToManyField(Jugador,default=None, null=True, blank=True, symmetrical=False)
	liga = models.ForeignKey(Liga, default=None, null=True) #un jugador pertenece a una unica liga
	alineacion=models.ManyToManyField(Jugador, related_name="jugador_alineacion" , default=None, null=True, blank=True, symmetrical=False) #aniadimos el related_name para volver aniadir un many to many con Jugador
	def __unicode__(self):
		return unicode(self.nombre)



class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	liga = models.ForeignKey(Liga, default=None, null=True) #un jugador pertenece a una unica liga
	equipo = models.ForeignKey(Equipo, default=None, null=True) #un equipo pertenece a un unico jugador

	def __unicode__(self):
		return self.user.username


class Jornada(models.Model):
	inicio= models.DateField(auto_now=False)
	fin= models.DateField(auto_now=False)
	nombre= models.CharField(max_length=150)

	def __unicode__(self):
		return self.nombre

#modelo creado para la actualizacion del mercado de fichajes y calculo de puntos
class Configurar(models.Model):
	fechaMercado= models.DateField(auto_now=True) #este campo ira cuando cualquier jugador entre en el juego la primera vez en el dia para controlar que se actualiza el mercado una vez al dia solo	
	fechaPuntos= models.DateField(auto_now=True) #fecha de la ultima actualizacion de los puntos de cada jugador
	ultimaJornada= models.OneToOneField(Jornada, null=True) #fecha de la ultima jornada jugada


#tabla que refleja los puntos que ha sacado un jugador en cada jornada
class PuntosJornada(models.Model):
	puntos= models.IntegerField(default=0)
	jornada= models.ForeignKey(Jornada, default=None)
	jugador= models.ForeignKey(Jugador, default=None)

	def __unicode__(self):
		return self.jugador.nombre  + " " + self.jugador.apellidos + " en " + self.jornada.nombre