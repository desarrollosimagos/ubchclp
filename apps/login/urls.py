from django.conf.urls import patterns, url
from .views import  logout_view, LoginUsuario
from django.contrib.auth.decorators import login_required


"""
    Urls a la plantilla de inicio de sesion
"""
urlpatterns = patterns('',
                       url(r'^$', LoginUsuario.as_view(), name='vista_login'),
                       url(r'^logout/$', logout_view, name='vista_logout'),
                       )