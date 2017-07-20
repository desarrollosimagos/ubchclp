from .models import Ubch
from .serializers import UbchSerializer
from rest_framework import viewsets


class UbchViewSet(viewsets.ModelViewSet):
    """ Clase que construye la vista de los `serializers`."""
    serializer_class = UbchSerializer
    queryset = Ubch.objects.all()
