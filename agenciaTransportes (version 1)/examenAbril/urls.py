from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView
from Entregas import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^menu_principal/$',views.estructura, name='estructura'),
    #destinatarios
    url(r'^ver_destinatarios/$',views.ver_destinatarios, name='ver_destinatarios'),
    url(r'^add_destinatario/$',views.add_destinatario, name='add_destinatario'),
    url(r'^search_destinatario/$',views.search_destinatario, name='search_destinatario'),
    #paquetes
	url(r'^ver_paquetes/$',views.ver_paquetes, name='ver_paquetes'),
    url(r'^add_paquete/$',views.add_paquete, name='add_paquete'),
    url(r'^search_paquete/$',views.search_paquete, name='search_paquete'),
    url(r'^modificar_paquete/$',views.modificar_paquete, name='modificar_paquete'),
    #usuarios
	url(r'^registrar/$',views.registro,name='registro'),
	url(r'^$',views.login,name='login'),
	url(r'^logout/$',views.logout_view, name='logout'),
    #vistas como clases para rutas
    url(r'^ver_rutas/$',views.ver_rutas.as_view(), name='ver_rutas'),
    url(r'^add_ruta/$',views.add_ruta.as_view(), name='add_ruta'),
   
]