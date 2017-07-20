from rest_framework import serializers
from .models import ClpUBC
from apps.registro.models import Ubch


class ClpUbchSerializer(serializers.ModelSerializer):

    def buscar_ubch(self, obj):
        cod_ubch = obj.cod_ubch
        ubch = Ubch.objects.filter(cod_ubch=cod_ubch)[0].nom_ubch
        return ubch

    ubch = serializers.SerializerMethodField('buscar_ubch')

    class Meta:
        model = ClpUBC
        fields = ('id', 'cod_ubch', 'ubch')
