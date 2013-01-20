#encoding:utf-8
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from principal.models import Idea, Comentario, Tarea, TareaxIdea, Aplicacion, Calificacion, TransaccionTiempo

class ContactoForm(forms.Form):
	correo = forms.EmailField(label='Tu correo electrónico')
	mensaje = forms.CharField(widget=forms.Textarea)

class IdeaForm(ModelForm):
	class Meta:
		model = Idea

class ComentarioForm(ModelForm):
	class Meta:
		model = Comentario
			
class TareaForm(ModelForm):
	class Meta:
		model = Tarea
			
class TareaIdeaForm(ModelForm):
	class Meta:
		model = TareaxIdea								

class AplicacionForm(ModelForm):
	class Meta:
		model = Aplicacion								

class CalificacionForm(ModelForm):
	class Meta:
		model = Calificacion

class TransaccionForm(ModelForm):
	class Meta:
		model = TransaccionTiempo

