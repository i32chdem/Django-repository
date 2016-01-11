# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, logout, login as auth_login
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
#para vistas basadas en clases
from django.views.generic.base import View
from django.views.generic import TemplateView

@login_required
def estructura(request):
	return render(request,"estructura.html")

def ver_destinatarios(request):
	destinatarios= Destinatario.objects.all()
	context={'destinatarios':destinatarios}
	return render(request,"ver_destinatarios.html",context)

@login_required
def add_destinatario(request):
	mensaje=""
	if request.method == 'POST':
		form= destinatarioForm(request.POST)
		if form.is_valid():
			x= form.save(commit=False) #commit=False hace que no se guarde aun el formulario
			try: #si existe, no guardamos otro destinatario igual
				destinatario= Destinatario.objects.get(nombre=x.nombre, direccion=x.direccion, ciudad=x.ciudad, codigo_postal=x.codigo_postal)
				mensaje="El destinatario ya existe"
			except ObjectDoesNotExist: #si no existe, lo guardamos
				form.save()
				mensaje="Destinatario guardado con exito"
	else:
		form= destinatarioForm(request.POST)
	destinatarios= Destinatario.objects.all()
	context={'form':form, 'destinatarios':destinatarios, 'mensaje':mensaje}
	return render(request,"add_destinatario.html",context)

def search_destinatario(request):
	destinatario=""
	if request.method == 'POST':
		form= buscarDestinatarioForm(request.POST)
		if form.is_valid():
			nombre= form.cleaned_data['nombre']
			destinatario= Destinatario.objects.filter(nombre=nombre)
	else:
		form= buscarDestinatarioForm()
	context={'form':form, 'destinatario':destinatario}
	return render(request,"search_destinatarios.html",context)

def ver_paquetes(request):
	paquetes= Paquete.objects.all()
	context={'paquetes':paquetes}
	return render(request,"ver_paquetes.html",context)

@login_required
def add_paquete(request):
	mensaje=""
	if request.method == 'POST':
		form= paqueteForm(request.POST)
		if form.is_valid():
			#guardamos automaticamente el paquete, ya que puede haber dos paquetes iguales hasta para la misma persona
			x=form.save()
			mensaje="Paquete añadido con exito"
	else:
		form= paqueteForm()
	context={'form':form, 'mensaje':mensaje}
	return render(request,"add_paquete.html",context)

def search_paquete(request):
	paquete=""
	if request.method == 'POST':
		form= buscarPaqueteForm(request.POST)
		if form.is_valid():
			contenido= form.cleaned_data['contenido']
			paquete= Paquete.objects.filter(contenido=contenido)
	else:
		form= buscarPaqueteForm()
	context={'form':form, 'paquete':paquete}
	return render(request,"search_paquete.html",context)

@login_required
def modificar_paquete(request):
	mensaje=""
	if request.method == 'POST':
		form= paqueteForm(request.POST)
		new_form= modifyPaqueteForm(request.POST)
		if form.is_valid() and new_form.is_valid():
			contenido = form.cleaned_data['contenido']
			valor = form.cleaned_data['valor']
			destinatario= form.cleaned_data['destinatario']

			new_contenido = new_form.cleaned_data['new_contenido']
			new_valor = new_form.cleaned_data['new_valor']
			try: #si el paquete que quiere modificar existe
				paquete=Paquete.objects.get(contenido=contenido, valor=valor, destinatario=destinatario)				
				paquete.contenido=new_contenido
				paquete.valor=new_valor
				paquete.save()
				mensaje="Paquete modificado con exito"
			except ObjectDoesNotExist: #si no existe
				mensaje="El paquete que quieres modificar no existe"
	else:
		form= paqueteForm()
		new_form= modifyPaqueteForm()
	context={'form':form, 'new_form':new_form, 'mensaje':mensaje}
	return render(request,"modificar_paquete.html",context)

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

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


class ver_rutas(View):
	template_name="ver_rutas.html"

	def get(self, request, *args, **kwargs):
		rutas=Ruta.objects.all()
		return render(request, self.template_name, {'rutas':rutas})

class add_ruta(View):
	template_name= "add_ruta.html"
	form_class= rutaForm

	def get(self, request, *args, **kwargs):
		form= self.form_class()
		return render(request, self.template_name, {'form':form})

	def post(self, request, *args, **kwargs):
		mensaje=""
		form= self.form_class(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			mensaje="Ruta añadida con exito"
		return render(request, self.template_name, {'form':form, 'mensaje':mensaje})