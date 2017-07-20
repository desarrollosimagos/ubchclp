from django.conf.urls import patterns, url
from .views import login_view, logout_view, RegistrarUsuario
from django.contrib.auth.decorators import login_required


"""
    Urls a la plantilla de inicio de sesion
"""
urlpatterns = patterns('',
                       url(r'^$', login_view, name='vista_login'),
                       url(r'^logout/$', logout_view, name='vista_logout'),
                       url(r'^nuevo_usuario/$',
                           login_required(RegistrarUsuario.as_view(), login_url='/'),
                           name="nuevo_usuario",
                           ),
                       )
