from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView
from viajes import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.estructura, name='estructura'),
	url(r'^ver_destinos/$',views.verDestinos, name='ver_destinos'),
    url(r'^destinos/$',views.destinos, name='destinos'),
	url(r'^buscar_destinos/$',views.buscarDestino, name='buscar_destinos'),
	url(r'^ver_viajes/$',views.verViajes, name='ver_viajes'),
    url(r'^viajes/$',views.viajes, name='viajes'),
	url(r'^buscar_viaje/$',views.buscarViaje, name='buscar_viaje'),
	url(r'^modificar_viaje/$',views.modificarViaje, name='modificar_viaje'),
	url(r'^registrar/$',views.registro,name='registro'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout_view, name='logout_view'),
    #urls de vistas basadas en clases
	url (r'^ver_rutas', views.rutas.as_view(), name='rutas'),
	url (r'^rutas', views.addRutas.as_view(), name='add_rutas'),
	url (r'^buscar_rutas', views.buscarRuta.as_view(), name='buscar_rutas'),

]
