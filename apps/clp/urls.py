from django.conf.urls import patterns, url
from .views import ListarView, ListarClpCedula, ListarClpCodigo
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
                       url(r'^listar/$', login_required(ListarView.as_view(), login_url='/'), name="listar_clp"),
                       url(r'^data/', 'apps.clp.views.load_data', name="datos_clp",),
                       url(r'^cedula=(?P<cedula>\d+)$',
                           login_required(ListarClpCedula.as_view(), login_url='/'),
                           name="list_registro",
                           ),
                       url(r'^codigo=(?P<codigo>\d+)$',
                           login_required(ListarClpCodigo.as_view(), login_url='/'),
                           name="list_registro",
                           ),
                       )
