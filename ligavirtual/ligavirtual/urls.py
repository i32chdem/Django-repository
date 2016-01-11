"""ligavirtual URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from ligamanager import views

from django.contrib.auth.views import login, logout #incorporada para el login


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.base, name='base'),
    url(r'^logout$',views.logout_view, name='logout'),
    url(r'^index$',views.index, name='index'),
    url(r'^registro$',views.registro, name='registro'),
	url(r'^editar$',views.editar_view, name='editar'),
    url(r'^crear_liga$',views.crearLiga_view, name='crearLiga'),
    url(r'^entrar_liga$',views.entrarLiga_view, name='entrarLiga'),
    url(r'^entrar_liga/crear_equipo$',views.crearEquipo_view, name='crearEquipo'),
    url(r'^plantilla$',views.plantilla_view, name='plantilla'),
    url(r'^clasificacion$',views.clasificacion_view, name='clasificacion'),
    url(r'^mercado_fichajes$',views.fichajes_view, name='fichajes'),
    url(r'^alineacion$',views.alineacion_view, name='alineacion'),
    url(r'^jornadas$',views.jornadas_view, name='jornadas'),
]





