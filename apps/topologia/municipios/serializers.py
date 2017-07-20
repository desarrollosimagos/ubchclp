from rest_framework.serializers import ModelSerializer
from .models import Municipio
from apps.topologia.estados.serializers import EstadoSerializer


class MunicipioSerializer(ModelSerializer):
    cod_estado = EstadoSerializer(many=False, read_only=True)
    
    class Meta:
        model = Municipio
        fields = ('id', 'municipio', 'estado', 'cod_estado')

    def __unicode__(self):
        return self.municipio
