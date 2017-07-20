from rest_framework.serializers import ModelSerializer
from .models import Estado
#from .serializers import EstadoSerializer


class EstadoSerializer(ModelSerializer):
    class Meta:
        #estado = EstadoSerializer(many=False, read_only=False)
        model = Estado
        fields = ('id', 'estado')
