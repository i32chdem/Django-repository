# -*- coding: utf-8 -*-
import os,sys

directorio=os.getcwd() #obtenemos el directorio actual

# ruta a nuestro archivo CSV
jornadas=directorio+"/jornadas.csv"
csv_filepathname=jornadas

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
    if row[0] != 'JORNADA': # ignoramos la primera línea del archivo CSV
        jornada = Jornada()
        jornada.inicio = row[0]
        jornada.fin = row[1]
        jornada.nombre = row[2]
        jornada.save()
