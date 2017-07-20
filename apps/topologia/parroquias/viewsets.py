from rest_framework.viewsets import ModelViewSet
from .serializers import ParroquiaSerializer
from .models import Parroquia


class ParroquiaViewset(ModelViewSet):
    serializer_class = ParroquiaSerializer
    queryset = Parroquia.objects.all()
