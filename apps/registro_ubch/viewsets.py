from rest_framework import viewsets
from .models import UnoPorDiez
from serializer import UnoPorDiezSerializer


class UnoPorDiezViewSet(viewsets.ModelViewSet):
    """ Clase que construye la vista de los `serializers`."""
    serializer_class = UnoPorDiezSerializer
    queryset = UnoPorDiez.objects.all()
