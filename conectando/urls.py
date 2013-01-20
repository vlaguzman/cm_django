from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'principal.views.inicio', name='home'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$','django.views.static.serve', {'document_root':settings.MEDIA_ROOT,}),
    url(r'^usuarios/$','principal.views.usuarios'),
    url(r'^contacto/$','principal.views.contacto'),
    url(r'^comenta/$','principal.views.nuevo_comentario'),
    url(r'^usuario/nuevo$','principal.views.nuevo_usuario'),
    url(r'^ingresar/$','principal.views.ingresar'),
    url(r'^privado/$','principal.views.privado'),
    url(r'^cerrar/$','principal.views.cerrar'),

    url(r'^ideas/$','principal.views.lista_ideas'),
    url(r'^misideas/$','principal.views.lista_ideas_usuario'),
    url(r'^idea/(?P<id_idea>\d+)$','principal.views.detalle_idea'),
    url(r'^miidea/(?P<id_idea>\d+)$','principal.views.detalle_idea_usuario'),
    url(r'^idea/nueva/$','principal.views.nueva_idea'),
    url(r'^tarea/nueva/$','principal.views.nueva_tarea'),
    url(r'^aceptar_propuesta/(?P<id_aplicacion>\d+)$','principal.views.aceptar_propuesta'),

    if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
   
)
