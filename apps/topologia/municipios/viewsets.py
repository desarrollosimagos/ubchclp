from rest_framework import viewsets
from .serializers import MunicipioSerializer
from .models import Municipio


class MunicipioViewSet(viewsets.ModelViewSet):
    serializer_class = MunicipioSerializer
    queryset = Municipio.objects.all()
