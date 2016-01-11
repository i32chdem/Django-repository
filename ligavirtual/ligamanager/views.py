# -*- encoding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from ligamanager.models import *
from forms import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.db.models import Max #para usar las consultas Max

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth.hashers import make_password #incluir para el make password
import random # para generar numeros aleatorios

from django.core.paginator import Paginator, InvalidPage, EmptyPage #para la paginacion 

#para el control del tiempo
from datetime import datetime, date, time, timedelta
import calendar

# VARIABLES "GLOBALES" PARA EL MAXIMO DE PORTEROS, DEFENSAS, CENTRO CAMPISTAS Y DELANTEROS
MAX_PORTEROS= 3
MAX_DEFENSAS= 8
MAX_CENTRO= 8
MAX_DELANTEROS= 5

#pagina principal donde inicias sesion 
def base(request):
	# Si el usuario esta ya logueado, lo redireccionamos a index_view
    if request.user.is_authenticated():
        return redirect(reverse('index'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
            	#logeamos al usuario
                login(request, user)
                #redireccionamos a la pagina de inicio de la partida
                return redirect(reverse('index'))
            else:
                # Redireccionar informando que la cuenta esta inactiva
     			messages.error(request, 'Tu cuenta de usuario esta inactiva')
        messages.error(request, 'Nombre de usuario o contraseña no valido')
    return render(request, 'login.html')


#vista para el registro de un nuevo jugador
def registro(request):
	form = registroForm(request.POST)  # A form bound to the POST data

	if request.method == 'POST':  # si le ha dado al boton del formulario...
		form = registroForm(request.POST)  # si el metodo es POST obtenemos los datos del usuario
		if form.is_valid():  # si todas las reglas de validacion se cumplen
  
            # En caso de ser valido, obtenemos los datos del formulario.
			username = form.cleaned_data["username"] #comprueba si ya existe en la DB
			password = form.cleaned_data["password"] #comprueba que coincidan las contraseñas
			email = form.cleaned_data["email"]
			first_name = form.cleaned_data["first_name"]
			last_name = form.cleaned_data["last_name"]
 			
			# E instanciamos un objeto User, con el username y password
			user_model = User.objects.create_user(username=username, password=password)
			# Añadimos el email
			user_model.email = email
			# Y guardamos el objeto, esto guardara los datos en la db.
			user_model.save()
			# Ahora, creamos un objeto UserProfile
			user_profile = UserProfile()
			# Al campo user le asignamos el objeto user_model
			user_profile.user = user_model

			user_profile.save()

			messages.success(request, 'Te has registrado con exito')
			# Ahora, redireccionamos a la pagina principal
			return redirect(reverse('index'))
	else:
		form = registroForm()
	
	return render_to_response("registro.html", {'form': form},context_instance=RequestContext(request))


def logout_view(request):
	logout(request)
	messages.success(request, 'Te has desconectado con exito.')
	return redirect(reverse('base'))

#funcion que calcula los puntos de cada jugador de la liga
def calcularPuntosJugadores(request):
	jugadores= Jugador.objects.all() #guardamos todos los jugadores
	for jugador in jugadores: #recorremos todos los jugadores
		lista= PuntosJornada.objects.filter(jugador=jugador)
		resultado=0
		for jornada in lista:
			resultado= resultado+ jornada.puntos
			jugador.puntos= resultado
			jugador.save()

#funcion que me organiza el mercado de fichajes de todas las ligas
def organizaFichajes(request):
	ligas= Liga.objects.all() #me devuelve todas las ligas
	lista=[]
	for liga in ligas: #recorremos todas las ligas
		equipos= Equipo.objects.filter(liga=liga) #me devuelve todos los equipos que pertenecen a una liga
		for equipo in equipos: #recorro todos los equipos
			jugadores= equipo.jugador.all() #me devuelve en lista, todos los jugadores del equipo
			for jugador in jugadores: #recorro todos los jugadores de un equipo
				lista.append(jugador) #inserto al final de lista todos los jugadores de equipos de una liga

		jugadoresTotal= Jugador.objects.all()
		fichajes=[] #lista de los jugadores libres
		for x in jugadoresTotal: #recorremos todos los jugadores de la BBDD
			libre= 1

			for y in lista: #recorremos todos los jugadores de la liga
				if x == y: #si pertenece a algun equipo
					libre= 0

			if libre == 1:
				fichajes.append(x) #insertamos en la lista fichajes, todos los jugadores libres

		liga.mercadoFichajes.clear() #borramos el anterior mercado de fichajes, por que si no lo que hace es añadirse jugadores al anterior

		for i in range(5):
			aux= random.choice(fichajes) #me devuelve un objeto de tipo Jugador al azar de fichajes
			liga.mercadoFichajes.add(aux) #guardamos los jugadores que habra en el mercado de fichajes
			fichajes.remove(aux) #lo eliminamos de la lista de fichajes para que no se repita

def puntosEquipo(request, jornada):
	equipos= Equipo.objects.all()
	puntos=0
	for equipo in equipos: #recorro todos los equipos
		alineacion= equipo.alineacion.all() #me devuelve en lista, los jugadores de la alineacion
		for jugador in alineacion: #recorro todos los jugadores de un equipo
			try: 
				puntosJornada= PuntosJornada.objects.get(jugador=jugador, jornada=jornada) #buscamos los puntos de todos los jugadores en esa jornada
				puntos = puntos + puntosJornada.puntos #sumo sus puntos
			except ObjectDoesNotExist:
				pass
		puntos= puntos+equipo.puntos #le sumamos lo calculado de la jornada a los que ya tenia
		equipo.puntos= puntos #le guardamos a cada equipo sus puntos
		equipo.dinero= equipo.dinero + (puntos * 10000) #cada punto que consiga en una jornada se le suman 10000€ de presupuesto al equipo de recompensa 
		equipo.save()

#pagina principal una vez hayas iniciado sesion con algun jugador
@login_required
def index(request):
	usuario= request.user.userprofile
	if request.method == 'POST':
		form = noticiaForm(request.POST)
		if form.is_valid(): #si es valido el formulario de cambiar los datos
			if usuario.liga != None:
				contenido= form.cleaned_data['contenido']
				if contenido != "":
					liga= usuario.liga
					noticia= Noticia()
					noticia.contenido= contenido
					noticia.autor= request.user
					noticia.save()

					liga.noticia.add(noticia)
			else:
				messages.warning(request,"El tablon de noticias estara desactivado mientras no pertenezcas a una liga")
	else:
		form = noticiaForm()

	lista=[]
	if usuario.liga != None:
		liga= usuario.liga
		lista= liga.noticia.all().order_by("-fecha") #devuelve todas las noticias de esa liga ordenado por la fecha mas cercana

		if usuario.equipo != None: #si el usuario tiene equipo
			############## CALCULAREMOS LOS PUNTOS DE CADA JUGADOR Y ACTUALIZAMOS EL MERCADO DE FICHAJES UNA VEZ AL DIA  #############
			#la primera vez que entre en el dia la primera persona que se conecte a la pagina tardara mas en cargas despues ya va fluido para todos
			fecha= Configurar.objects.all() #ponemos en fecha todos los objetos Configurar
		
			if not fecha: #si no hay ninguno creamos uno
				date = Configurar()
				date.save()

			fecha= Configurar.objects.get() #ponemos en aux el unico objeto Configurar que hay
			aux= str(fecha.fechaPuntos) #convertimos en string la fecha de la ultima vez que se actualizo el mercado

			hoy= datetime.now() #guardamos en hoy la fecha de hoy
			hoy= hoy.strftime("%Y-%m-%d") # fecha con formato AÑO-MES-DIA

			if aux < hoy: #si la fecha de la ultima actualizacion es anterior a hoy
				fecha.save() #guardamos la fecha de hoy como ultima vez actualizado
				organizaFichajes(request) #ORGANIZAMOS EL MERCADO DE FICHAJES
			################################################################################################################


			############### CALCULAMOS LOS PUNTOS DE LA ALINEACION TITULAR DEL EQUIPO AL FINAL DE LA JORNADA ###############
			try:
				ultima= Jornada.objects.filter(fin__lte=hoy).aggregate(Max('fin'))['fin__max'] #me devuelve la jornada ultima que ha acabado antes de hoy
				ultima= Jornada.objects.get(fin=ultima)

				if fecha.ultimaJornada != ultima:
					try: #si hay puntoscalculados para esa jornada
						aux= PuntosJornada.objects.filter(jornada=ultima)
						calcularPuntosJugadores(request) #CALCULAMOS LOS PUNTOS DE TODOS LOS JUGADORES
						puntosEquipo(request, ultima) #CALCULAMOS LOS PUNTOS DE LA ULTIMA JORNADA
						fecha.ultimaJornada= ultima
						fecha.save()
					except ObjectDoesNotExist:
						pass
			except ObjectDoesNotExist:
						pass
			################################################################################################################

	paginator= Paginator(lista, 5) #paginamos las noticias de 5 en 5
	try: 
		pagina= int(request.GET.get("page",'1'))
	except ValueError: pagina = 1

	try:
		lista= paginator.page(pagina)
	except (InvalidPage, EmptyPage):
		lista= paginator.page(paginator.num_pages)

	return render(request, 'index.html',{'form':form, 'lista':lista})


#vista para la edicion de los datos de un usuario
@login_required
def editar_view(request):
	correo= request.user.email
	nombre= request.user.first_name
	apellidos= request.user.last_name

	if request.method == 'POST':
		form = editarForm(request.POST, request=request)
		formPass = changePasswordForm(request.POST)
		
		if form.is_valid(): #si es valido el formulario de cambiar los datos
			request.user.email = form.cleaned_data['email'] #cogemos los datos de email
			request.user.first_name = form.cleaned_data['first_name']
			request.user.last_name = form.cleaned_data['last_name']

			request.user.save() #lo guardamos en la base de datos

			if request.user.email != correo:
				messages.success(request, 'El email ha sido cambiado con exito!.')
			if request.user.first_name != nombre:
				messages.success(request, 'El Nombre ha sido cambiado con exito!.')
			if request.user.last_name != apellidos:
				messages.success(request, 'Los apellidos ha sido cambiado con exito!.')
			
		if formPass.is_valid(): #si es valido el formulario de cambiar la contraseña
			request.user.password = make_password(formPass.cleaned_data['password']) 
			request.user.save()
			messages.success(request, 'La contraseña ha sido cambiado con exito!.')
			messages.success(request, 'Es necesario introducir los datos para entrar.')
			return redirect(reverse('editar')) #da igual a donde redireccione por que va a tener que logearte de nuevo
		
	else:
		form = editarForm(
			request=request,
			initial= {'last_name':request.user.last_name, 'email':request.user.email, 'first_name':request.user.first_name})
		formPass = changePasswordForm()

	return render(request, 'editar.html', {'form': form, 'formPass':formPass})

#funcion que me organiza el mercado de fichajes de todas las ligas
def organizaPrimerMercado(request, liga):
	lista=[]
	equipos= Equipo.objects.filter(liga=liga) #me devuelve todos los equipos que pertenecen a una liga
	for equipo in equipos: #recorro todos los equipos
		jugadores= equipo.jugador.all() #me devuelve en lista, todos los jugadores del equipo
		for jugador in jugadores: #recorro todos los jugadores de un equipo
			lista.append(jugador) #inserto al final de lista todos los jugadores de equipos de una liga

	jugadoresTotal= Jugador.objects.all()
	fichajes=[] #lista de los jugadores libres
	for x in jugadoresTotal: #recorremos todos los jugadores de la BBDD
		libre= 1

		for y in lista: #recorremos todos los jugadores de la liga
			if x == y: #si pertenece a algun equipo
				libre= 0

		if libre == 1:
			fichajes.append(x) #insertamos en la lista fichajes, todos los jugadores libres

	liga.mercadoFichajes.clear() #borramos el anterior mercado de fichajes, por que si no lo que hace es añadirse jugadores al anterior

	for i in range(5):
		aux= random.choice(fichajes) #me devuelve un objeto de tipo Jugador al azar de fichajes
		liga.mercadoFichajes.add(aux) #guardamos los jugadores que habra en el mercado de fichajes
		fichajes.remove(aux) #lo eliminamos de la lista de fichajes para que no se repita

#vista para crear una liga
@login_required
def crearLiga_view(request):

	if request.method == 'POST':
		form = crearLigaForm(request.POST)
		if form.is_valid():
			nombre = form.cleaned_data['nombre'] 
			password = form.cleaned_data["password"]
			liga = Liga()
			liga.nombre = nombre
			liga.password = password
			liga.save()
			organizaPrimerMercado(request,liga)
			messages.success(request, 'Liga creada correctamente!.')
	else:
		form = crearLigaForm()

	return render(request, 'crearLiga.html', {'form': form})	


#vista para entrar a formar parte de una liga un cliente
@login_required
def entrarLiga_view(request):

	usuario= request.user.userprofile #guardamos en usuario el UserProfile del usuario logeado en este momento
	if usuario.liga != None: #controla que no pueda volver a entrar a una liga dicho usuario
		messages.error(request, 'Ya perteneces a una liga.')
		return redirect(reverse('index')) #redireccionamos a la pagina principal

	if request.method == 'POST':
		form = entrarLigaForm(request.POST)
		if form.is_valid():
			nombre = form.cleaned_data['nombre']
			liga= Liga.objects.get(nombre=nombre) #me devuelve en liga, la Liga con el nombre introducido por el usuario
			usuario.liga= liga #le guardamos dicha liga al usuario
			usuario.save()
			messages.success(request, 'Has entrado correctamente a la liga!.')	
			messages.success(request, '¡Ya puedes crear tu equipo!.')					
			return redirect(reverse('crearEquipo')) #redireccionamos a la pagina de crear equipo
	else:
		form = entrarLigaForm()

	return render(request, 'entrarLiga.html', {'form': form})	

#funcion que te devuelve 1 si existe el jugador en otro equipo de la misma liga y 0 en caso contrario
def existeJugador(request, aux):
	liga= request.user.userprofile.liga #obtenemos la liga del jugador registrado
	equipos= Equipo.objects.filter(liga=liga) #obtenemos todos los equipos de esa liga
	for team in equipos: #recorremos todos los equipos de esa liga
		jugadores= team.jugador.all() #me devuelve en jugadores todos los jugadores del equipo
		for player in jugadores: #recorremos todos los jugadores de un equipo
			if aux == player: #si coincide, devolvemos 1
				return 1
	return 0


def asignarJugadores(request):

	equipo= request.user.userprofile.equipo

	lista= Jugador.objects.filter(posicion= "P") #me devuelve en lista todos los Porteros
	aux= random.choice(lista) #me devuelve un objeto de tipo Jugador al azar de esa lista
	while existeJugador(request,aux) == 1:
		aux= random.choice(lista) #me devuelve un objeto de tipo Jugador al azar de esa lista
	equipo.jugador.add(aux) #añadimos el elemento aux a equipo.jugador (No hace falta hacer un save despues)
	

	lista= Jugador.objects.filter(posicion= "D") #me devuelve en lista todos los Defensas
	for i in range(4):
		aux= random.choice(lista) #me devuelve un objeto de tipo Jugador al azar de esa lista
		while existeJugador(request,aux) == 1:
			aux= random.choice(lista) #me devuelve un objeto al azar de esa lista
		equipo.jugador.add(aux) #añadimos el elemento aux a equipo.jugador (No hace falta hacer un save despues)

	lista= Jugador.objects.filter(posicion= "MC") #me devuelve en lista todos los Mediocentros
	for i in range(4):
		aux= random.choice(lista) #me devuelve un objeto de tipo Jugador al azar de esa lista
		while existeJugador(request,aux) == 1:
			aux= random.choice(lista) #me devuelve un objeto al azar de esa lista
		equipo.jugador.add(aux) #añadimos el elemento aux a equipo.jugador (No hace falta hacer un save despues)

	lista= Jugador.objects.filter(posicion= "DC") #me devuelve en lista todos los Delanteros
	for i in range(2):
		aux= random.choice(lista) #me devuelve un objeto de tipo Jugador al azar de esa lista
		while existeJugador(request,aux) == 1:
			aux= random.choice(lista) #me devuelve un objeto al azar de esa lista
		equipo.jugador.add(aux) #añadimos el elemento aux a equipo.jugador (No hace falta hacer un save despues)

#vista para crear un equipo un equipo
@login_required
def crearEquipo_view(request):

	usuario= request.user.userprofile #guardamos en usuario el UserProfile del usuario logeado en este momento
	team= Equipo()
	if usuario.liga == None: #si no tiene liga lo redireccionamos a entrarLiga
		messages.error(request, 'Aun no perteneces a ninguna liga, ¡unete a una liga y ya podras crear tu equipo!.')		
		return redirect(reverse('entrarLiga'))
	else:
		if request.method == 'POST':
			form = crearEquipoForm(request.POST)
			if form.is_valid():
				nombre = form.cleaned_data['nombre']
				if usuario.equipo == None: # si todavia no tiene equipo el jugador debe de crearlo
					team= Equipo() #creamos un objeto Equipo
					
					team.nombre= nombre #le ponemos nombre al equipo
					team.liga= request.user.userprofile.liga #le guardamos la liga a la que pertenece el usuario
					team.save() #guardamos el equipo en la BD

					usuario.equipo= team #le asignamos el equipo al jugador
					usuario.save() #guardamos el jugador en la BD

					asignarJugadores(request)

					messages.success(request, 'Has creado al equipo correctamente!.')
				else: # si ya tiene equipo puede modificar sus datos aqui
					team= Equipo.objects.get(nombre=request.user.userprofile.equipo) #obtenemos el equipo del jugador

					team.nombre=nombre #le cambiamos el nombre
					team.save() #lo guardamos en la BD
					messages.success(request, 'Has modificado el nombre de tu equipo correctamente!.')
		else:
			form = crearEquipoForm(
				request=request,
				initial= {'nombre':request.user.userprofile.equipo})
	return render(request, 'crearEquipo.html', {'form': form})	

#def totalPuntosJugador(request):
	

def venderJugador(request, jugador):
	usuario= request.user.userprofile
	equipo= usuario.equipo
	liga= usuario.liga
	presupuesto= equipo.dinero
	precio= jugador.precio

	presupuesto= presupuesto+precio
	equipo.dinero= presupuesto
	equipo.jugador.remove(jugador.id) #eliminamos el jugador del mercado del equipo
	equipo.save()
	cadena= "Mercado de Fichajes: He vendido al defensa "+ str(jugador)
	noticia= Noticia()
	noticia.contenido= cadena
	noticia.autor= request.user
	noticia.save()
	liga.noticia.add(noticia)
	messages.success(request, 'Has vendido correctamente al jugador.')


#vista para mostrar la plantilla actual de jugadores, permite tambien vender un jugador
@login_required
def plantilla_view(request):
	usuario= request.user.userprofile #guardamos en usuario el UserProfile del usuario logeado en este momento
	if usuario.liga == None: #si no tiene liga  lo redireccionamos a entrarLiga
		messages.error(request, 'Aun no perteneces a ninguna liga, ¡unete a una liga y ya podras crear tu equipo!.')		
		return redirect(reverse('entrarLiga'))
	else: 
		if usuario.equipo== None: #si no tienes equipo
			messages.error(request, 'Aun no tienes ningun equipo, !crea tu equipo ahora!.')		
			return redirect(reverse('crearEquipo'))
	
	lista= usuario.equipo.jugador.all().order_by('posicion') #me devuelve en lista, todos los jugadores del equipo del usuario registrado

	if request.method == 'POST':
		form = ofertaForm(request.POST)
		if form.is_valid():
			valor = request.POST['valor']
			player= request.POST['player']
			jugador= Jugador.objects.get(id=player)
			venderJugador(request, jugador)
	else:
		form = ofertaForm()

	presupuesto= usuario.equipo.dinero

	return render(request, 'plantilla.html',{'lista':lista, 'form':form, 'presupuesto':presupuesto})

#vista para mostrar la plantilla actual de jugadores
@login_required
def clasificacion_view(request):
	usuario= request.user.userprofile #guardamos en usuario el UserProfile del usuario logeado en este momento
	
	if usuario.liga == None: #si no tiene liga  lo redireccionamos a entrarLiga
		messages.error(request, 'Aun no perteneces a ninguna liga, ¡unete a una liga y ya podras crear tu equipo!.')		
		return redirect(reverse('entrarLiga'))
	else: 
		if usuario.equipo== None: #si no tienes equipo
			messages.error(request, 'Aun no tienes ningun equipo, !crea tu equipo ahora!.')		
			return redirect(reverse('crearEquipo'))
	
	liga= Liga.objects.get(nombre=usuario.liga) #me devuelve la liga del usuario
	
	equipos= Equipo.objects.filter(liga=liga).order_by('-puntos')
	
	return render(request, 'clasificacion.html',{'equipos':equipos})


def realizaFichaje(request, jugador):
	usuario= request.user.userprofile #guardamos en usuario el UserProfile del usuario logeado en este momento
	dinero= usuario.equipo.dinero #guardamos el dinero actual del usuario
	precio= jugador.precio #guardamos el precio que valor el jugador
	
	if dinero < precio: #si el usuario tiene menos dinero de lo que vale el jugador
			messages.error(request, 'No tienes dinero suficiente para realizar la oferta.')
	else: #si tiene dinero para ficharlo
		liga= usuario.liga
		mercado= liga.mercadoFichajes.all() #guardamos en mercado todos los jugadores que hay actualmente en el mercado de fichajes
		player= mercado.filter(nombre=jugador.nombre, apellidos=jugador.apellidos) #nos devuelve en player el jugador del mercado de fichajes
		if player == None:
			messages.error(request, 'El jugador que quieres fichar ya no esta en el mercado de fichajes.')
		else:
			equipo= usuario.equipo
			posicion= jugador.posicion
			jugadoresEquipo= usuario.equipo.jugador.all() #cogemos todos los jugadores del equipo
			lista= jugadoresEquipo.filter(posicion=posicion) #seleccionamos los que pertenecen a dicha posicion
			tam= len(lista) #contamos cuantos jugadores hay

			if posicion == "P":
				if tam < MAX_PORTEROS: # si no ha llegado al maximo de jugadores en esa posicion
					usuario.equipo.jugador.add(jugador) #añadimos el jugador al equipo
					liga.mercadoFichajes.remove(jugador.id) #eliminamos el jugador del mercado de fichajes
					equipo.dinero= usuario.equipo.dinero - jugador.precio #descontamos el dinero al usuario
					equipo.save()

					cadena= "Mercado de Fichajes: He fichado al portero "+ str(jugador)
					noticia= Noticia()
					noticia.contenido= cadena
					noticia.autor= request.user
					noticia.save()
					liga.noticia.add(noticia)
					messages.success(request, 'Has añadido un nuevo portero a tu equipo.')
				else:
					messages.error(request, 'No puedes fichar mas porteros, debes de vender alguno antes de fichar mas.')
			elif posicion == "D":
				if tam < MAX_DEFENSAS:
					usuario.equipo.jugador.add(jugador)
					liga.mercadoFichajes.remove(jugador.id)
					equipo.dinero= usuario.equipo.dinero - jugador.precio
					equipo.save()

					cadena= "Mercado de Fichajes: He fichado al defensa "+ str(jugador)
					noticia= Noticia()
					noticia.contenido= cadena
					noticia.autor= request.user
					noticia.save()
					liga.noticia.add(noticia)
					messages.success(request, 'Has añadido un nuevo defensa a tu equipo.')
				else:
					messages.error(request, 'No puedes fichar mas defensas, debes de vender alguno antes de fichar mas.')
			elif posicion == "MC":
				if tam < MAX_CENTRO:
					usuario.equipo.jugador.add(jugador)
					liga.mercadoFichajes.remove(jugador.id)
					equipo.dinero= usuario.equipo.dinero - jugador.precio
					equipo.save()

					cadena= "Mercado de Fichajes: He fichado al mediocentro "+ str(jugador)
					noticia= Noticia()
					noticia.contenido= cadena
					noticia.autor= request.user
					noticia.save()
					liga.noticia.add(noticia)
					messages.success(request, 'Has añadido un nuevo mediocentro a tu equipo.')
				else:
					messages.error(request, 'No puedes fichar mas mediocentros, debes de vender alguno antes de fichar mas.')
			elif posicion == "DC":
				if tam < MAX_DELANTEROS:
					usuario.equipo.jugador.add(jugador)
					liga.mercadoFichajes.remove(jugador.id)
					equipo.dinero= usuario.equipo.dinero - jugador.precio
					equipo.save()

					cadena= "Mercado de Fichajes: He fichado al delantero "+ str(jugador)
					noticia= Noticia()
					noticia.contenido= cadena
					noticia.autor= request.user
					noticia.save()
					liga.noticia.add(noticia)
					messages.success(request, 'Has añadido un nuevo delantero a tu equipo.')
				else:
					messages.error(request, 'No puedes fichar mas delanteros, debes de vender alguno antes de fichar mas.')


#vista para mostrar el mercado de fichajes
@login_required
def fichajes_view(request):
	usuario= request.user.userprofile #guardamos en usuario el UserProfile del usuario logeado en este momento
	if usuario.liga == None: #si no tiene liga  lo redireccionamos a entrarLiga
		messages.error(request, 'Aun no perteneces a ninguna liga, ¡unete a una liga y ya podras crear tu equipo!.')		
		return redirect(reverse('entrarLiga'))
	else: 
		if usuario.equipo== None: #si no tienes equipo
			messages.error(request, 'Aun no tienes ningun equipo, !crea tu equipo ahora!.')		
			return redirect(reverse('crearEquipo'))

	liga = Liga.objects.get(nombre= usuario.liga)
	lista= liga.mercadoFichajes.all() #devuelve la lista del mercado de fichajes de la liga
	 
	if request.method == 'POST':
		form = ofertaForm(request.POST)
		if form.is_valid():
			valor = request.POST['valor']
			player= request.POST['player']
			jugador= Jugador.objects.get(id=player)
			realizaFichaje(request, jugador)
	else:
		form = ofertaForm()

	presupuesto= usuario.equipo.dinero
	return render(request, 'fichajes.html', {'lista':lista, 'form':form, 'presupuesto':presupuesto})	

#funcion que añade un jugador a la alineacion titular
def alinearJugador(request, jugador):	
	usuario= request.user.userprofile
	equipo= usuario.equipo
	try:
   		equipo.alineacion.get(id=jugador.id)
   		messages.warning(request, 'El jugador ya esta en el once titular')
	except ObjectDoesNotExist: #si no existe objeto en la consulta anterior
		alineacion= equipo.alineacion.all() #guardamos en alineacion todos los jugadores de la alineacion titular
		if len(alineacion) >= 11: 
			messages.error(request, 'Ya tienes 11 jugadores en el equipo titular.')
		else: 
	 		if jugador.posicion == "P": #si qeremos alinear un portero
				try: 
					porteros= equipo.alineacion.filter(posicion="P") #me devuelve los porteros alineados
					messages.error(request, 'Ya tienes otro portero en el once, no puedes alinear mas de uno.')
				except ObjectDoesNotExist:
					usuario.equipo.alineacion.add(jugador) #añadimos el jugador a la alineacion
			else:
				usuario.equipo.alineacion.add(jugador) #añadimos el jugador a la alineacion


#funcion que elimina un jugador de la alineacion titular
def suplenteJugador(request, jugador):	
	usuario= request.user.userprofile
	if jugador != None: 
		usuario.equipo.alineacion.remove(jugador.id)
	else: #informamos de que no esta entre los titulares
		messages.warning(request, 'El jugador no se encuentra dentro del equipo titular.')


#vista para mostrar la alineacion titular de un equipo
@login_required
def alineacion_view(request):
	usuario= request.user.userprofile #guardamos en usuario el UserProfile del usuario logeado en este momento
	equipo= usuario.equipo #equipo del jugador logeado
	if usuario.liga == None: #si no tiene liga  lo redireccionamos a entrarLiga
		messages.error(request, 'Aun no perteneces a ninguna liga, ¡unete a una liga y ya podras crear tu equipo!.')		
		return redirect(reverse('entrarLiga'))
	else: 
		if usuario.equipo== None: #si no tienes equipo
			messages.error(request, 'Aun no tienes ningun equipo, !crea tu equipo ahora!.')		
			return redirect(reverse('crearEquipo'))
	
	############# CONSEGUIMOS QUE NO SE PUEDA CAMBIAR LA ALINACION UNA VEZ HAYA EMPEZADO LA JORNADA #############
	hoy= datetime.now() #guardamos la fecha de hoy
	jornada= Jornada.objects.filter(inicio__lte=hoy, fin__gte=hoy) # <= --> __lte=  y >= --> __gte
	####################################################################################################
	
	if request.method == 'POST':
		form = titularForm(request.POST)
		suplentes= suplenteForm(request.POST)
	
		if len(jornada)!=0:
			messages.error(request, 'La jornada ya ha empezado, no puedes cambiar la alinacion una vez empezada.')
		else:
			if form.is_valid():
				if 'elegido' in request.POST:
					elegido= request.POST['elegido'] #recogo el jugador 
					jugador= Jugador.objects.get(id=elegido)
					alinearJugador(request,jugador)
				else:
					elegido= None
						
			if suplentes.is_valid():
				if 'reserva' in request.POST:
					reserva= request.POST['reserva'] #recogo el jugador
					jugador= equipo.alineacion.get(id=reserva)
					suplenteJugador(request,jugador)
				else: 
					reserva= None
	else:
		form = titularForm()
		suplentes= suplenteForm()

	jugadores= usuario.equipo.jugador.all().order_by('posicion')
	titulares= usuario.equipo.alineacion.all().order_by('posicion')
	
	return render(request, 'alineacion.html', {'form':form, 'suplentes':suplentes, 'jugadores':jugadores, 'titulares':titulares})	

#vista para mostrar las jornadas
@login_required
def jornadas_view(request):
	jornadas= Jornada.objects.all()

	return render(request, 'jornadas.html', {'jornadas':jornadas})	