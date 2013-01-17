# Create your views here.
from principal.models import Idea, Comentario, Tarea, TareaxIdea, Aplicacion, Perfil, Calificacion, TransaccionTiempo
from principal.forms import IdeaForm, ComentarioForm, ContactoForm, TareaForm, TareaIdeaForm, AplicacionForm, CalificacionForm, TransaccionForm
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
			return HttpResponseRedirect('/privado')
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
	validar_transaccion = TransaccionTiempo.objects.filter(usuario=usuario)
	if not validar_transaccion:
		transaccion = TransaccionTiempo.objects.create(forma_adquisicion='Unidades iniciales', cantidad=3, usuario=usuario)
	return render_to_response('privado.html', {'usuario':usuario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/')

def contacto(request):
	if request.method=='POST':
		formulario = ContactoForm(request.POST)
		if formulario.is_valid():
			titulo = 'Mensaje desde conectando mentes'
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

@login_required(login_url='/ingresar')
def detalle_idea(request, id_idea):
	usuario = request.user
	idea_ = get_object_or_404(Idea, pk=id_idea)
	comentarios = Comentario.objects.filter(idea=idea_)
	tareas = TareaxIdea.objects.filter(idea=idea_)
	aplicaciones = Aplicacion.objects.all()
	calificaciones_like = Calificacion.objects.filter(idea=idea_, idea_clasificacion='Me gusta')
	calificaciones_dislike = Calificacion.objects.filter(idea=idea_, idea_clasificacion='No me gusta')
	calificacion_permitida = Calificacion.objects.filter(idea=idea_, usuario=usuario)
	if request.method=='POST':
		formulario_comentario = ComentarioForm(request.POST)
		if formulario_comentario.is_valid():
			formulario_comentario.save()
			return HttpResponseRedirect('/idea/'+id_idea)
	else:
		formulario_comentario = ComentarioForm()
	if request.method=='POST':
		formulario_aplicacion = AplicacionForm(request.POST)
		if formulario_aplicacion.is_valid():
			formulario_aplicacion.save()
			return HttpResponseRedirect('/idea/'+id_idea)
	else:
		formulario_aplicacion = AplicacionForm()	
	if request.method=='POST':
		formulario_calificacion = CalificacionForm(request.POST)
		if formulario_calificacion.is_valid():
			formulario_calificacion.save()
			return HttpResponseRedirect('/idea/'+id_idea)
	else:
		formulario_calificacion = CalificacionForm()	
	return render_to_response('idea.html',{'idea':idea_, 'comentarios':comentarios, 'calificacion_permitida':calificacion_permitida, 'calificaciones_dislike':calificaciones_dislike, 'calificaciones_like':calificaciones_like, 'usuario':usuario, 'tareas':tareas, 'aplicaciones':aplicaciones, 'formulario_comentario':formulario_comentario,'formulario_aplicacion':formulario_aplicacion, 'formulario_calificacion':formulario_calificacion}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def detalle_idea_usuario(request, id_idea):
	usuario = request.user
	idea_ = get_object_or_404(Idea, pk=id_idea)
	tareas = TareaxIdea.objects.filter(idea=idea_)
	aplicaciones = Aplicacion.objects.all()
	if request.method=='POST':
		formulario_tareaidea = TareaIdeaForm(request.POST)
		if formulario_tareaidea.is_valid():
			formulario_tareaidea.save()
			return HttpResponseRedirect('/ideas')
	else:
		formulario_tareaidea = TareaIdeaForm()
	return render_to_response('miidea.html',{'idea':idea_, 'tareas':tareas, 'formulario_tareaidea':formulario_tareaidea, 'usuario':usuario, 'aplicaciones':aplicaciones}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def nueva_idea(request):
	usuario = request.user
	if request.method=='POST':
		formulario_ideas = IdeaForm(request.POST, request.FILES)
		formulario_tareas = TareaForm(request.POST, request.FILES)
		if formulario_ideas.is_valid():
			formulario_ideas.save()
			return HttpResponseRedirect('/ideas')
	else:
		formulario_ideas = IdeaForm()
		formulario_tareas = TareaForm()
	return render_to_response('ideaform.html',{'formulario_ideas':formulario_ideas, 'usuario':usuario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def nueva_tarea(request):
	usuario = request.user
	if request.method=='POST':
		formulario_tareas = TareaForm(request.POST, request.FILES)
		if formulario_tareas.is_valid():
			formulario_tareas.save()
			return HttpResponseRedirect('/ideas')
	else:
		formulario_tareas = TareaForm()
	return render_to_response('tareaform.html',{'formulario_tareas':formulario_tareas}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def lista_ideas_usuario(request):
	usuario = request.user
	ideas = Idea.objects.all()
	return render_to_response('misideas.html', {'ideas':ideas, 'usuario':usuario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def nueva_tareaxidea(request, id_idea):
	idea_ = get_object_or_404(Idea, pk=id_idea)
	if request.method=='POST':
		formulario_tareaidea = TareaIdeaForm(request.POST)
		if formulario_tareaidea.is_valid():
			formulario_tareaidea.save()
			return HttpResponseRedirect('/ideas')
	else:
		formulario_tareaidea = TareaIdeaForm()
	return render_to_response('tareaideaform.html',{'idea':idea_, 'formulario_tareaidea':formulario_tareaidea}, context_instance=RequestContext(request))
