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
	titulo = models.CharField(max_length=100, verbose_name='Título', unique=True)
	descripcion = models.TextField(verbose_name='Descripción', help_text='Descripción de la idea')
	imagen = models.ImageField(upload_to='recetas', verbose_name='Imágen')
	tiempo_registro = models.DateTimeField(auto_now=True)
	usuario = models.ForeignKey(User)

	def __unicode__(self):
		return self.titulo

class Comentario(models.Model):
	idea = models.ForeignKey(Idea)
	texto = models.TextField(help_text='Tu comentario', verbose_name='Comentario')

	def __unicode__(self):
		return self.texto

class Tarea(models.Model):
	descripcion = models.TextField(verbose_name='Descripción', help_text='Descripción de la idea')
	
	def __unicode__(self):
		return self.texto

class TareaxIdea(models.Model):
	idea = models.ForeignKey(Idea)
	tarea = models.ForeignKey(Tarea)
	tiempo_registro = models.DateTimeField(auto_now=True)
	unidades_pago = models.IntegerField()
	tiempo_estimado = models.IntegerField()


