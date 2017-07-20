from rest_framework import viewsets
from .models import Patrullero
from .serializer import PatrulleroSerializer, PatrulleroDatosSerializer


class UnoPorDiezViewSet(viewsets.ModelViewSet):
    """ Clase que construye la vista de los `serializers`."""
    serializer_class = PatrulleroSerializer
    queryset = Patrullero.objects.all()


class PatrullerosDatosViewSet(viewsets.ModelViewSet):
    """ Clase que construye la vista de los `serializers`."""
    serializer_class = PatrulleroDatosSerializer
    queryset = Patrullero.objects.all()
