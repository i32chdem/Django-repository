#Fichero para aniadir los formularios
# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User #importa el modelo user
from ligamanager.models import * #importa los modelos creados 
from django.forms import widgets

from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from django.contrib.auth.hashers import make_password #incluir para el make password

from django.core.exceptions import ObjectDoesNotExist #para el except ObjectDoesNotExist

class registroForm(forms.Form):
	username = forms.CharField(label= 'Nombre de Usuario:', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Usuario', 'label':'Usuario'}), required=True)
	email = forms.EmailField(label= 'email:', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'email'}), required=True)
	password = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}), required=True)
	password2 = forms.CharField(label='Repita la Password:', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}), required=True)
	first_name= forms.CharField(label='Nombre:', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nombre'}), required=False)
	last_name= forms.CharField(label='Apellidos:',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Apellidos'}), required=False)

	def clean_username(self):
		#Comprueba que no exista un username igual en la db (siempre hay que obtener el diccionario de datos)
		diccionario = self.cleaned_data
		username = diccionario.get('username') 
		if User.objects.filter(username=username):
			raise forms.ValidationError('Nombre de usuario ya registrado.') #imprime automaticamente este mensaje cuando ocurre el if
		return username

	def clean_password2(self):
		#Comprueba que password y password2 sean iguales.
		diccionario = self.cleaned_data
		password = diccionario.get('password')
		password2 = diccionario.get('password2')
		if password != password2:
			raise forms.ValidationError('Las contraseñas no coinciden.')
		return password2

class loginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Usuario'}), required=True)
	password = forms.CharField( widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}), required=True)


class editarForm(forms.Form):
	email = forms.EmailField(label= 'email:', widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)
	first_name= forms.CharField(label='Nombre:', widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
	last_name= forms.CharField(label='Apellidos:',widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)

	def __init__(self, *args, **kwargs): #sobreescribimos el método __init__ del formulario para poder definir la QuerySet dinámicamente cuando se crea un formulario.
    	#obtener request
		self.request = kwargs.pop('request')
		return super(editarForm,self).__init__(*args, **kwargs)

class changePasswordForm(forms.Form):
	password = forms.CharField(label='Nueva Password:', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
	password2 = forms.CharField(label='Repita la nueva Password:', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

	def clean_password2(self):
		#Comprueba que password y password2 sean iguales.
		password = self.cleaned_data['password']
		password2 = self.cleaned_data['password2']
		if password != password2:
			raise forms.ValidationError('Las contraseñas no coinciden.')
		return password2

class crearLigaForm(forms.Form):
	nombre =  forms.CharField(label='Nombre Liga:', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Liga'}), required=True)
	password =  forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}), required=True)
	password2 =  forms.CharField(label='Vuelve a introducir la Password:', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}), required=True)

	def clean_password2(self):
		#Comprueba que password y password2 sean iguales.
		password = self.cleaned_data['password']
		password2 = self.cleaned_data['password2']
		if password != password2:
			raise forms.ValidationError('Las contraseñas no coinciden.')
		return password2

	def clean_nombre(self):
		#Comprueba que no exista el nombre de la liga ya en la base de datos
		diccionario = self.cleaned_data
		nombre = diccionario.get('nombre') 
		if Liga.objects.filter(nombre=nombre):
			raise forms.ValidationError('Nombre de liga ya insertado.') #imprime automaticamente este mensaje cuando ocurre el if
		return nombre

class entrarLigaForm(forms.Form):
	nombre =  forms.CharField(label='Nombre Liga:', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Liga'}), required=True)
	password =  forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}), required=True)

	def clean_password(self):
		#Comprueba que es la password correcta de dicha liga
		if self.is_valid():
			nombre = self.cleaned_data['nombre']
			#password = make_password(self.cleaned_data['password'])
			password = self.cleaned_data['password']
			liga = Liga.objects.get(nombre=nombre) #buscamos la liga con dicho nombre
			if liga.password != password:
				raise forms.ValidationError('Las contraseñas no es correcta.')
			return password

	def clean_nombre(self):
		#Comprueba que exista el nombre de la liga ya en la base de datos
		nombre = self.cleaned_data['nombre']
		try:
			Liga.objects.get(nombre=nombre)
		except ObjectDoesNotExist: #si no existe el objeto que hemos buscado salta un assert ObjectDoesNotExist
			raise forms.ValidationError('No existe una liga con dicho nombre') #imprime automaticamente este mensaje cuando ocurre el if
		return nombre

class crearEquipoForm(forms.Form): 
	nombre = forms.CharField(label='Nombre Equipo:', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Equipo'}), required=True)
	def __init__(self, *args, **kwargs): #sobreescribimos el método __init__ del formulario para poder definir la QuerySet dinámicamente cuando se crea un formulario.
		self.request = kwargs.pop('request','request')
		return super(crearEquipoForm,self).__init__(*args, **kwargs)

	def clean_nombre(self): #comprueba que no existe en esa liga otro equipo con ese nombre
		nombre = self.cleaned_data['nombre']
		if Equipo.objects.filter(nombre=nombre):
			raise forms.ValidationError('Ya existe un equipo con este nombre.')
		return nombre

class noticiaForm(forms.Form):
	contenido= forms.CharField(label='Noticia:', widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)

class ofertaForm(forms.Form):
	valor= forms.BooleanField(label='', required=False, widget=forms.TextInput(attrs={'type':'hidden'}))

class titularForm(forms.Form):
	titular= forms.BooleanField(label='', required=False, widget=forms.TextInput(attrs={'type':'hidden'}))

class suplenteForm(forms.Form):
	suplente= forms.BooleanField(label='', required=False, widget=forms.TextInput(attrs={'type':'hidden'}))
