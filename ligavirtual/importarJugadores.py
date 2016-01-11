# -*- coding: utf-8 -*-
import os,sys

directorio=os.getcwd() #obtenemos el directorio actual

# ruta a nuestro archivo CSV
aux=directorio+"/jornadas.csv"
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
    if row[0] != 'JUGADOR': # ignoramos la primera línea del archivo CSV
        jugadores = Jugador()
        jugadores.nombre = row[0]
        jugadores.apellidos = row[1]
        jugadores.posicion = row[2]
        jugadores.precio = row[3]
        jugadores.save()
