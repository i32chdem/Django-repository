# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login as auth_login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
#para vistas basadas en clases
from django.views.generic.base import View
from django.views.generic import TemplateView

def estructura(request):
	return render(request, "estructura.html")
	
def ver_destinatarios(request):
	destinatarios= Destinatario.objects.all()
	context={'destinatarios':destinatarios}
	return render (request, "ver_destinatarios.html",context)

@login_required	
def add_destinatario(request):
	mensaje=""
	if request.method=="POST":
		form= destinatarioForm(request.POST)
		if form.is_valid():
			x=form.save(commit=False)
			try: #si el objeto ya existe
				destinatario=Destinatario.objects.get(nombre=x.nombre, direccion=x.direccion, ciudad=x.ciudad, codigo_postal=x.codigo_postal)
				mensaje="El destinatario ya se encuentra en la Base de Datos"
			except ObjectDoesNotExist:
				form.save() #guardamos el objeto en la base de datos
				mensaje="Destinatario añadido con exito"
	else:
		form= destinatarioForm()
	context={'form':form, 'mensaje':mensaje}
	return render(request, "add_destinatario.html",context)
	
def search_destinatario(request):
	if request.method=="POST":
		form= searchDestinatarioForm(request.POST)
		if form.is_valid():
			x=form.save(commit=False)
			if Destinatario.objects.filter(nombre=x.nombre):
				destinatarios=Destinatario.objects.filter(nombre=x.nombre)
				context={'destinatarios':destinatarios, 'form':form}
				return render(request, "search_destinatario.html", context)
			else:
				mensaje="El destinatario buscado no existe"
				print mensaje
				context={'mensaje':mensaje, 'form':form}
				return render(request, "search_destinatario.html", context)
	else:
		form=searchDestinatarioForm()
	context={'form':form}
	return render(request, "search_destinatario.html", context)
	
def ver_paquetes(request):
	paquetes= Paquete.objects.all()
	context={'paquetes':paquetes}
	return render (request, "ver_paquetes.html", context)

@login_required	
def add_paquete(request):
	mensaje=""
	if request.method=="POST":
		form=paqueteForm(request.POST)
		if form.is_valid():
			form.save() #guardamos el paquete
			mensaje="Paquete almacenado con exito"
	else:
		form=paqueteForm()
	context={'form':form, 'mensaje':mensaje}
	return render(request, "add_paquete.html", context)

def search_paquete(request):
	if request.method=="POST":
		form= searchPaqueteForm(request.POST)
		if form.is_valid():
			x=form.save(commit=False)
			paquetes= Paquete.objects.filter(contenido=x.contenido)
			if paquetes:
				context= {'form':form, 'paquetes':paquetes}
				return render(request, "search_paquete.html", context)
			else:
				mensaje="El paquete buscado no se encuentra en la Base de Datos"
				context= {'form':form, 'mensaje':mensaje}
				return render(request, "search_paquete.html", context)
	else:
		form= searchPaqueteForm(request.POST)
	context={'form':form}
	return render (request, "search_paquete.html",context)

@login_required		
def editar_paquete(request, pk):
	paquete = get_object_or_404(Paquete, pk=pk)
	if request.method=="POST":
		form= paqueteForm(request.POST, instance= paquete)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	else:
		form = paqueteForm(instance = paquete)
		context = {'form':form}
	return render_to_response('editar_paquete.html', context,  context_instance=RequestContext(request))


def registro(request):
    form = registroForm(request.POST) 
    if request.method == 'POST': 
        form = registroForm(request.POST) 
        if form.is_valid(): 
            username = form.cleaned_data["username"] 
            password = form.cleaned_data["password"] 

            user_model = User.objects.create_user(username=username, password=password)
            user_model.save()
            mensaje="Te has registrado con exito"
            return redirect(reverse("login"))
    else:
        form = registroForm()
    return render_to_response("registro.html", {'form': form},context_instance=RequestContext(request))


def login(request):
    mensaje=""
    # Si el usuario esta ya logueado, lo redireccionamos a index_view
    if request.user.is_authenticated():
        return redirect(reverse('estructura'))
    if request.method == 'POST':
        form= loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"] 
            password = form.cleaned_data["password"] 
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    #logeamos al usuario
                    auth_login(request, user)
                    #redireccionamos a la pagina de inicio de la partida
                    return redirect(reverse('estructura'))
                else:
                    mensaje="Tu cuenta de usuario esta inactiva"
            mensaje="Nombre de usuario o password no valido"
    else:
        form = loginForm()
    context={'mensaje':mensaje, 'form':form}
    return render(request, 'login.html',context)


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))
    
class ver_rutas(View):
	template_name= "ver_rutas.html"
	
	def get(self, request, *args, **kwargs):
		rutas= Ruta.objects.all()
		context={'rutas':rutas}
		return render(request,self.template_name,context)
		
class add_ruta(View):
	template_name= "add_ruta.html"
	form_class= rutaForm
	
	def get(self, request, *args, **kwargs):
		form= self.form_class()
		context={'form':form}
		return render(request, self.template_name, context)
			
	def post(self, request, *args, **kwargs):
		form= self.form_class(request.POST, request.FILES)
		if form.is_valid():
			form.save()
		context={'form':form}
		return render(request, self.template_name, context)
	
class search_ruta(View):
	template_name="search_ruta.html"
	form_class= searchRutaForm
	
	def get(self, request, *args, **kwargs):
		form= self.form_class()
		context={'form':form}
		return render(request, self.template_name, context)
			
	def post(self, request, *args, **kwargs):
		form= self.form_class(request.POST, request.FILES)
		if form.is_valid():
			x= form.save(commit=False)
			rutas= Ruta.objects.filter(nombre=x.nombre)
			if rutas:
				context={'form':form,'rutas':rutas}
				return render(request, self.template_name, context)
			else:
				mensaje="No hay ninguna ruta con dicho nombre"
				context={'form':form, 'mensaje':mensaje}
				return render(request, self.template_name, context)
		context={'form':form}
		return render(request, self.template_name, context)

