from django.conf.urls import url
from .views import RegistrarMunicipio, ActualizarMunicipio, EliminarMunicipio,ListarMunicipio, load_data # Importamos las Vistas


urlpatterns = [
    url(r'^registrar_municipio/', 'apps.topologia.municipios.views.RegistrarMunicipio', name="registrar_municipio",),
    url(r'^actualizar_municipio/(?P<pk>\d+)/$', 'apps.topologia.municipios.views.ActualizarMunicipio', name='actualizar_municipio',),
    url(r'^eliminar_municipio/(?P<pk>\d+)/$', 'apps.topologia.municipios.views.EliminarMunicipio', name='eliminar_municipio',),
    url(r'^listar_municipios/$','apps.topologia.municipios.views.ListarMunicipio', name='listar_municipio',),
    url(r'^data/', 'apps.topologia.municipios.views.load_data', name="datos_municipio",), # URL de Exportacion para la data
]
