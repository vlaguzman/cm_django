# Create your views here.
from principal.models import Idea, Comentario, Tarea, TareaxIdea, Aplicacion, PerfilxUsuario, Perfil
from principal.forms import IdeaForm, ComentarioForm, ContactoForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

def inicio(request):
	ideas = Idea.objects.all()
	return render_to_response('inicio.html', {'ideas':ideas}, context_instance=RequestContext(request))

def usuarios(request):
	usuarios = User.objects.all()
	ideas = Idea.objects.all()
	return render_to_response('usuarios.html',{'usuarios':usuarios, 'ideas':ideas}, context_instance=RequestContext(request))

def nuevo_usuario(request):
	if request.method=='POST':
		formulario = UserCreationForm(request.POST)
		if formulario.is_valid:
			formulario.save()
			return HttpResponseRedirect('/')
	else:
		formulario = UserCreationForm()
	return render_to_response('nuevousuario.html', {'formulario':formulario}, context_instance=RequestContext(request))

def ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/privado')
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/privado')
				else:
					return render_to_response('noactivo.html', context_instance=RequestContext(request))
			else:
				return render_to_response('nousuario.html', context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))							

@login_required(login_url='/ingresar')
def privado(request):
	usuario = request.user
	return render_to_response('privado.html', {'usuario':usuario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/')

def contacto(request):
	if request.method=='POST':
		formulario = ContactoForm(request.POST)
		if formulario.is_valid():
			titulo = 'Mensaje desde el recetario de Maestros del Web'
			contenido = formulario.cleaned_data['mensaje'] + "\n"
			contenido += 'Comunicarse a: ' + formulario.cleaned_data['correo']
			correo = EmailMessage(titulo, contenido, to=['guzman.vla@gmail.com'])
			correo.send()
			return HttpResponseRedirect('/')
	else:
		formulario = ContactoForm
	return render_to_response('contactoform.html',{'formulario':formulario}, context_instance=RequestContext(request))

def nuevo_comentario(request):
	if request.method=='POST':
		formulario = ComentarioForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/ideas')
	else:
		formulario = ComentarioForm()
	return render_to_response('comentarioform.html', {'formulario':formulario}, context_instance=RequestContext(request))

def lista_ideas(request):
	ideas = Idea.objects.all()
	return render_to_response('ideas.html', {'ideas':ideas}, context_instance=RequestContext(request))

def detalle_idea(request):
	idea_ = get_object_or_404(Idea, pk=id_idea)
	comentarios = Comentario.objects.filter(idea=idea_)
	return render_to_response('idea.html',{'receta':idea_, 'comentarios':comentarios}, context_instance=RequestContext(request))

def nueva_idea(request):
	if request.method=='POST':
		formulario = RecetaForm(request.POST, request.FILES)
		if formulario.is_valid:
			formulario.save()
			return HttpResponseRedirect('/ideas')
	else:
		formulario = RecetaForm()
	return render_to_response('ideaform.html',{'formulario':formulario}, context_instance=RequestContext(request))



