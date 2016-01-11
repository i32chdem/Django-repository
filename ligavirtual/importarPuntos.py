# -*- coding: utf-8 -*-
import os,sys

directorio=os.getcwd() #obtenemos el directorio actual

# ruta a nuestro archivo CSV
aux=directorio+"/puntos.csv"
csv_filepathname=aux

# ruta a nuestro proyecto de django
proyecto=directorio+"/ligavirtual"
your_djangoproject_home=proyecto

sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# importamos nuestro modelo
from ligamanager.models import *

import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

for row in dataReader:
    if row[0] != 'PuntosJornada': # ignoramos la primera línea del archivo CSV
        jornada = PuntosJornada()
        player= Jugador.objects.get(nombre=row[0], apellidos=row[1])
        jornada.jugador = player
        partidos= Jornada.objects.get(nombre=row[2])
      	jornada.jornada = partidos
	jornada.puntos = row[3]
        jornada.save()
