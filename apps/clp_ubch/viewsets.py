from rest_framework import viewsets
from .models import ClpUBC
from .serializer import ClpUbchSerializer


class ClpUbchViewSet(viewsets.ModelViewSet):
    """ Clase que construye la vista de los `serializers`."""
    serializer_class = ClpUbchSerializer
    queryset = ClpUBC.objects.all()
