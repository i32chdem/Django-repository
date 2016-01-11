from django.forms import ModelForm
from django import forms
from .models import * 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class addDestinoForm(forms.ModelForm):
	class Meta:
		model= Destino
		fields = '__all__'

class buscarDestinoForm(forms.ModelForm):
	class Meta:
		model= Destino
		fields = ('lugar',)

class ViajeForm(forms.ModelForm):
	class Meta:
		model= Viaje
		fields = '__all__'

class modificarViajeForm(forms.Form):
	new_dias = forms.IntegerField(label="Nuevos dias:")
	new_coste = forms.IntegerField(label="Nuevo coste:")
	new_desplazamiento = forms.CharField(max_length=100, label="Nuevo desplazamiento:")

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

class rutasForm(forms.ModelForm):
	class Meta:
		model= Ruta
		fields = '__all__'

class buscarRutaForm(forms.ModelForm):
	class Meta:
		model= Ruta
		fields= ('nombre',)