from django.forms import ModelForm
from django import forms
from .models import * 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class destinatarioForm(forms.ModelForm):
	class Meta:
		model= Destinatario
		fields= '__all__'

class buscarDestinatarioForm(forms.ModelForm):
	class Meta:
		model= Destinatario
		fields= ('nombre',)

class paqueteForm(forms.ModelForm):
	class Meta:
		model= Paquete
		fields= '__all__'

class buscarPaqueteForm(forms.ModelForm):
	class Meta:
		model= Paquete
		fields= ('contenido',)

class modifyPaqueteForm(forms.Form):
	new_contenido = forms.CharField (max_length = 128, label="Nuevo contenido:")
	new_valor = forms.IntegerField (label="Nuevo valor:")

class registroForm(forms.Form):
	username= forms.CharField(label="Nombre de usuario:", required=True)
	password= forms.CharField(label="Password",required=True, widget=forms.PasswordInput())
	password2= forms.CharField(label="Repita Password",required=True, widget=forms.PasswordInput())

	def clean_username(self):
		username= self.cleaned_data.get("username")
		if User.objects.filter(username=username):
			raise forms.ValidationError("Nombre de usuario ya registrado")
		return username

	def clean_password2(self):
		password=self.cleaned_data.get("password")
		password2=self.cleaned_data.get("password2")
		if password != password2:
			raise forms.ValidationError("Las password no coinciden")
		return password2

class loginForm(forms.Form):
	username= forms.CharField(label="Nombre:", required=True)
	password= forms.CharField(label="Password",required=True, widget=forms.PasswordInput())

class rutaForm(forms.ModelForm):
	class Meta:
		model= Ruta 
		fields= '__all__'