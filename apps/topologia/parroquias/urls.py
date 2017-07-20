from django.conf.urls import url
from .views import RegistrarParroquia, ActualizarParroquia, EliminarParroquia, ListarParroquia, BuscarAjaxMun, BuscarAjaxPar, load_data_parroquia


urlpatterns = [
    url(r'^registrar_parroquia/$', 'apps.topologia.parroquias.views.RegistrarParroquia'),
    url(r'^actualizar_parroquia/(?P<pk>\d+)/$', 'apps.topologia.parroquias.views.ActualizarParroquia', name='actualizar_parroquia',),
    url(r'^eliminar_parroquia/(?P<pk>\d+)/$', 'apps.topologia.parroquias.views.EliminarParroquia', name='eliminar_parroquia',),
    url(r'^listar_parroquia/$','apps.topologia.parroquias.views.ListarParroquia', name='listar_parroquia',),
    url(r'^busqueda_ajax/$','apps.topologia.parroquias.views.BuscarAjaxMun', name='listar_parroquia',),
    url(r'^busqueda_ajax2/$','apps.topologia.parroquias.views.BuscarAjaxPar', name='listar_municipios',),
    url(r'^data/', 'apps.topologia.parroquias.views.load_data_parroquia', name="datos_parroquia",), # URL de Importacion para la data
]
