from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from apps.topologia.estados.viewsets import EstadoViewSet
from apps.topologia.municipios.viewsets import MunicipioViewSet
from apps.topologia.parroquias.viewsets import ParroquiaViewset
from apps.centro_votacion.viewsets import CentroVotacionViewSet
from apps.registro.viewsets import RegistroViewSet


router = DefaultRouter()
router.register(r'estados', EstadoViewSet)
router.register(r'municipios', MunicipioViewSet)
router.register(r'parroquias', ParroquiaViewset)
router.register(r'centro_votacion', CentroVotacionViewSet)
router.register(r'registro_electoral', RegistroViewSet)
urlpatterns = patterns('',
                       url(r'^', include(router.urls))
                       )
