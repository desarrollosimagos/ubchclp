from rest_framework import serializers
from .models import UnoPorDiez
from apps.registro.models import Ubch


class UnoPorDiezSerializer(serializers.ModelSerializer):

    def buscar_ubch(self, obj):
        cod_ubch = obj.cod_ubch
        ubch = Ubch.objects.filter(cod_ubch=cod_ubch)[0].nom_ubch
        #print "PARROQUIA: ",parroquias
        return ubch

    ubch = serializers.SerializerMethodField('buscar_ubch')

    class Meta:
        model = UnoPorDiez
        fields = ('id', 'cedula', 'p_nombre', 's_nombre', 'p_apellido',
                  's_apellido', 'telefono', 'twitter', 'cod_ubch', 'ubch')
