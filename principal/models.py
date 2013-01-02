from django.db import models
from django.contrib.auth.models import User

class Idea(models.Model):
	IDEA_CALIFICACION_OPCIONES = (
       	(ME_GUSTA, 'Me_gusta'),
       	(NO_ME_GUSTA, 'No_me_gusta'),
    )
    idea_clasificacion = models.CharField(max_length=2,
                                      choices=IDEA_CALIFICACION_OPCIONES,
                                      default=ME_GUSTA)	
	nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
	descripcion = models.TextField(verbose_name='Descripción', help_text='Descripción de la idea')
	imagen = models.ImageField(upload_to='ideas', verbose_name='Imágen')
	fecha_registro = models.DateTimeField(auto_now=True)
	usuario = models.ForeignKey(User)

	def __unicode__(self):
		return self.nombre

class Comentario(models.Model):
	idea = models.ForeignKey(Idea)
	texto = models.TextField(help_text='Tu comentario', verbose_name='Comentario')

	def __unicode__(self):
		return self.texto

class Tarea(models.Model):
	perfil = models.ForeignKey(Perfil)
	nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
	descripcion = models.TextField(verbose_name='Descripción', help_text='Descripción de la tarea')

	def __unicode__(self):
		return self.nombre

class TareaxIdea(models.Model):
	tarea = models.ForeignKey(Tarea)
	idea = models.ForeignKey(Idea)
	fecha_creacion = models.DateTimeField(auto_now=True)
	unidades_pago = models.IntegerField()
	tiempo_estimado = models.IntegerField()

class Aplicacion(models.Model):
	usuario = models.ForeignKey(User)
	tarea = models.ForeignKey(Tarea)
	fecha_aplicacion = models.DateTimeField(auto_now=True)
	comentario = models.TextField(help_text='Tu comentario', verbose_name='Comentario')

class PerfilxUsuario(models.Model):
	usuario = models.ForeignKey(User)
	perfil = models.ForeignKey(Perfil)

class Perfil(models.Model):
	nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
	descripcion = models.TextField(verbose_name='Descripción')
		
	def __unicode__(self):
		return self.nombre
