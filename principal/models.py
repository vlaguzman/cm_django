#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

class Idea(models.Model):
	IDEA_CLASIFICACION_OPCIONES = (
       	('Emprendimiento digital', 'digital'),
       	('Emprendimiento tradicional', 'tradicional'),
       	('Emprendimiento cultural', 'cultural'),
       	('Emprendimiento social', 'social'),
    )
	idea_clasificacion = models.CharField(max_length=30, choices=IDEA_CLASIFICACION_OPCIONES)
	nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
	descripcion = models.TextField(verbose_name='Descripción', help_text='Descripción de la idea')
	imagen = models.ImageField(upload_to='ideas', verbose_name='Imágen')
	fecha_registro = models.DateTimeField(auto_now=True)
	usuario = models.ForeignKey(User)

	def __str__(self):
		return self.nombre

	def __unicode__(self):
		return u"%s - %s" % (self.nombre, self.descripcion)

	class Meta:
		ordering = ["nombre"]

class Comentario(models.Model):
	idea = models.ForeignKey(Idea)
	usuario = models.ForeignKey(User)
	texto = models.TextField(help_text='Tu comentario', verbose_name='Comentario')
	
	def __str__(self):
		return self.texto

	def __unicode__(self):
		return self.texto

class Calificacion(models.Model):
	IDEA_CALIFICACION_OPCIONES = (
       	('S', 'Me_gusta'),
       	('N', 'No_me_gusta'),
    )
	idea_clasificacion = models.CharField(max_length=2, choices=IDEA_CALIFICACION_OPCIONES)
	idea = models.ForeignKey(Idea)
	usuario = models.ForeignKey(User)

	def __unicode__(self):
		return self.texto

class Perfil(models.Model):
	nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
	descripcion = models.TextField(verbose_name='Descripción')
	usuarios =  models.ManyToManyField(User, null=True, blank=True)
	
	def __str__(self):
		return self.nombre

	def __unicode__(self):
		return self.nombre

	class Meta:
		ordering = ["nombre"]
		
class Tarea(models.Model):
	perfil = models.ForeignKey(Perfil)
	nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
	descripcion = models.TextField(verbose_name='Descripción', help_text='Descripción de la tarea')
	
	def __str__(self):
		return self.nombre
	
	def __unicode__(self):
		return self.nombre

	class Meta:
		ordering = ["nombre"]

class TareaxIdea(models.Model):
	TAREA_ESTADOS = (
    	('Sin asignar', 'Sin_asignar'),
    	('Asignada', 'Asignada'),
    	('Terminada', 'Terminada'),
	)
	estado = models.CharField(max_length=20, choices=TAREA_ESTADOS)
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
