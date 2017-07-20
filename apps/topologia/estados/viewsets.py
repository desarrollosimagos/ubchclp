from rest_framework import viewsets
from .serializers import EstadoSerializer
from .models import Estado


class EstadoViewSet(viewsets.ModelViewSet):
    serializer_class = EstadoSerializer
    queryset = Estado.objects.all()
