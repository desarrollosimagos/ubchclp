from django.conf.urls import patterns, url
from .views import ListarView, RegistroView, UbchListView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
                       url(r'^listar/$', login_required(ListarView.as_view(), login_url='/'), name="listar_ubch"),
                       url(r'^data/', 'apps.registro.views.load_data', name="datos_ubch",),
                       url(r'^cedula=(?P<cedula>\d+)$', RegistroView.as_view(),
                           name="list_registro",),
                       url(r'^codigo=(?P<cod_ubch>\d+)$',
                           login_required(UbchListView.as_view(), login_url='/'),
                           name="list_ubch",
                           ),
                       )
