from .models import Clp
from .serializers import ClpSerializer
from rest_framework import viewsets


class ClpViewSet(viewsets.ModelViewSet):
    """ Clase que construye la vista de los `serializers`."""
    serializer_class = ClpSerializer
    queryset = Clp.objects.all()
