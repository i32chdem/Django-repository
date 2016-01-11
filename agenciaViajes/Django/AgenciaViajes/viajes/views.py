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
    return render (request, "estructura.html")

def verDestinos(request):
    destinos=Destino.objects.all()
    context= {'destinos':destinos}
    return render(request, 'ver_destinos.html', context)  

@login_required
def destinos(request):
    mensaje=""
    if request.method == 'POST':
        form = addDestinoForm(request.POST)
        if form.is_valid():
            lugar = form.cleaned_data['lugar'] 
            descripcion = form.cleaned_data["descripcion"]
            distancia = form.cleaned_data["distancia"]

            try:
                destino=Destino.objects.get(lugar=lugar)
                mensaje="Dicho destino ya esta añadido"
            except ObjectDoesNotExist:
                destino=Destino()
                destino.lugar=lugar
                destino.descripcion=descripcion
                destino.distancia=distancia
                destino.save()
                mensaje="Destino añadido con exito"
    else:
        form = addDestinoForm()

    destinos=Destino.objects.all()
    context= {'form': form, 'mensaje':mensaje, 'destinos':destinos}
    return render(request, 'destinos.html', context)    

def buscarDestino(request):
    mensaje=""
    if request.method == 'POST':
        form = buscarDestinoForm(request.POST)
        if form.is_valid():
            lugar = form.cleaned_data['lugar'] 

            try:
                destinos=Destino.objects.get(lugar=lugar)
                context= {'form': form, 'mensaje':mensaje, 'destinos':destinos}
                return render(request, 'buscar_destinos.html', context)     
            except ObjectDoesNotExist:
                mensaje="Dicho destino no existe"
    else:
        form = buscarDestinoForm()

    context= {'form': form, 'mensaje':mensaje}
    return render(request, 'buscar_destinos.html', context)  

def verViajes(request):
    viajes=Viaje.objects.all()
    context= {'viajes':viajes}
    return render(request, 'ver_viajes.html', context)    

@login_required
def viajes(request):
    mensaje=""
    if request.method == 'POST':
        form = ViajeForm(request.POST)
        if form.is_valid():
            destino = form.cleaned_data["destino"]
            dias = form.cleaned_data["dias"]
            coste = form.cleaned_data["coste"]
            desplazamiento = form.cleaned_data["desplazamiento"]

            try: 
                viaje= Viaje.objects.get(destino=destino, dias=dias, coste=coste, desplazamiento=desplazamiento)
                mensaje="Este mismo viaje ya existe"
            except ObjectDoesNotExist:
                form.save()
    else:
        form = ViajeForm()

    viajes=Viaje.objects.all()
    context= {'form': form, 'viajes':viajes, 'mensaje':mensaje}
    return render(request, 'viajes.html', context)  

def buscarViaje(request):
    mensaje=""
    if request.method == 'POST':
        form = ViajeForm(request.POST)
        if form.is_valid():
            destino = form.cleaned_data['destino'] 
            dias = form.cleaned_data['dias'] 
            coste = form.cleaned_data['coste'] 
            desplazamiento = form.cleaned_data['desplazamiento'] 
            try:
                viaje=Viaje.objects.get(destino=destino, dias=dias, coste=coste, desplazamiento=desplazamiento)
                context= {'form': form, 'viaje':viaje}
                return render(request, 'buscar_viaje.html', context)
            except ObjectDoesNotExist:
                mensaje="El viaje buscado no existe"
    else:
        form = ViajeForm()

    context= {'form': form, 'mensaje':mensaje}
    return render(request, 'buscar_viaje.html', context) 

@login_required
def modificarViaje(request):
    mensaje=""
    if request.method == 'POST':
        form = ViajeForm(request.POST)
        nuevo = modificarViajeForm(request.POST)
        if form.is_valid() and nuevo.is_valid():
            destino = form.cleaned_data['destino'] 
            dias = form.cleaned_data['dias'] 
            coste = form.cleaned_data['coste'] 
            desplazamiento = form.cleaned_data['desplazamiento'] 

            new_dias = nuevo.cleaned_data['new_dias'] 
            new_coste = nuevo.cleaned_data['new_coste'] 
            new_desplazamiento = nuevo.cleaned_data['new_desplazamiento']
            try:
                viaje=Viaje.objects.get( dias=dias, coste=coste, desplazamiento=desplazamiento)
                try:
                    nuevo_viaje=Viaje.objects.get(destino=destino, dias=new_dias, coste=new_coste, desplazamiento=new_desplazamiento)
                    mensaje="Los datos del viaje modificados ya existen"
                except ObjectDoesNotExist:
                    viaje.dias= new_dias
                    viaje.coste= new_coste
                    viaje.desplazamiento= new_desplazamiento
                    viaje.save()
                    mensaje="Viaje modificado con exito"
            except ObjectDoesNotExist:
                mensaje="El viaje que quieres modificar no existe"
    else:
        form = ViajeForm()
        nuevo = modificarViajeForm()

    context= {'form': form, 'nuevo':nuevo, 'mensaje':mensaje}
    return render(request, 'modificar_viaje.html', context) 

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

class rutas(View):
    template_name = 'ver_rutas.html'
    def get(self, request, *args, **kwargs):
        rutas = Ruta.objects.all()
        return render(request, self.template_name, {'rutas':rutas})


class addRutas(View):
    template_name= "rutas.html"
    form_class= rutasForm

    def get(self, request, *args, **kwargs):
        form= self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form= self.form_class(request.POST, request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]

            try:
                ruta=Ruta.objects.get(nombre=nombre)
                mensaje="Ya existe una ruta con este nombre"
                return render(request, self.template_name, {'form':form, 'mensaje':mensaje})
            except ObjectDoesNotExist:
                form.save()
                mensaje="Ruta añadida con exito"
            return render(request, self.template_name, {'form':form, 'mensaje':mensaje})
        return render(request, self.template_name, {'form':form})

class buscarRuta(View):
    template_name="buscar_ruta.html"
    form_class= buscarRutaForm

    def get(self, request, *args, **kwargs):
        form= self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form= self.form_class(request.POST, request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            try:
                ruta=Ruta.objects.get(nombre=nombre)
                return render(request, self.template_name, {'form':form, 'ruta':ruta})
            except ObjectDoesNotExist:
                mensaje="La ruta buscada no existe"
            return render(request, self.template_name, {'form':form, 'mensaje':mensaje})
        return render(request, self.template_name, {'form':form})
