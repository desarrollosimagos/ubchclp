from django.conf.urls import url
from .views import RegistrarEstado ,ActualizarEstado, EliminarEstado,ListarEstado, base_view, load_data

urlpatterns = [
    url(r'^registrar_estado/$','apps.topologia.estados.views.RegistrarEstado'),
    url(r'^actualizar_estado/(?P<pk>\d+)/$','apps.topologia.estados.views.ActualizarEstado', name='actualizar_estado'),
    url(r'^eliminar_estado/(?P<pk>\d+)/$', 'apps.topologia.estados.views.EliminarEstado'),
    #url(r'^registrar_estado/', RegistrarEstado.as_view(), name="registrar_estados",),
    #url(r'^actualizar_estado/(?P<pk>\d+)/$', ActualizarEstado.as_view(), name='actualizar_estado',),
    #url(r'^eliminar_estado/(?P<pk>\d+)/$', EliminarEstado.as_view(), name='eliminar_estado',),
    url(r'^$', 'apps.topologia.estados.views.base_view', name="home",), # URL de Exportacion para la data
    url(r'^lista_estado/$','apps.topologia.estados.views.ListarEstado',name='listar_estados',),
    url(r'^data/', 'apps.topologia.estados.views.load_data', name="datos_estados",), # URL de Exportacion para la data
]
