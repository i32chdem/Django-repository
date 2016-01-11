from django.conf.urls import patterns, include, url
from django.contrib import admin
from Entregas import views 
admin.autodiscover()
urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', views.estructura, name="estructura"),
	#destinatario
	url(r'^ver_destinatarios/$', views.ver_destinatarios, name="ver_destinatarios"),
	url(r'^add_destinatario/$', views.add_destinatario, name="add_destinatario"),
	url(r'^search_destinatario/$', views.search_destinatario, name="search_destinatario"),
	#paquetes
	url(r'^ver_paquetes/$', views.ver_paquetes, name="ver_paquetes"),
	url(r'^add_paquete/$', views.add_paquete, name="add_paquete"),
	url(r'^search_paquete/$', views.search_paquete, name="search_paquete"),
	url(r'^ver_paquetes/(?P<pk>[0-9]+)/editar/$', views.editar_paquete, name='editar_paquete'),
	#usuario
	url(r'^registrar/$',views.registro,name='registro'),
	url(r'^login/$',views.login,name='login'),
	url(r'^logout/$',views.logout_view, name='logout_view'),
	#vistas basadas en clases para ruta
	url (r'^ver_rutas', views.ver_rutas.as_view(), name='ver_rutas'),
	url (r'^add_rutas', views.add_ruta.as_view(), name='add_rutas'),
	url (r'^buscar_rutas', views.search_ruta.as_view(), name='buscar_rutas'),
)
