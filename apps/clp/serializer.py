# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Clp
from apps.topologia.estados.serializers import EstadoSerializer
from apps.topologia.municipios.serializers import MunicipioSerializer
from apps.topologia.parroquias.serializers import ParroquiaSerializer
from apps.topologia.estados.models import Estado
from apps.topologia.municipios.models import Municipio
from apps.topologia.parroquias.models import Parroquia


class ClpSerializer(serializers.ModelSerializer):

    parroquia = serializers.SerializerMethodField('calculo_cod_parr')  # Metodo para arrojar el string de parroquia
    municipio = serializers.SerializerMethodField('calculo_cod_mun')  # Metodo para arrojar el string de municipio
    estado = serializers.SerializerMethodField('calculo_cod_est')  # Metodo para arrojar el string de estado
    nac = serializers.SerializerMethodField('calculo_nac')
    sexo = serializers.SerializerMethodField('calculo_sexo')

    class Meta:
        model = Clp
        fields = (
            'id',
            'nac',
            'cedula',
            'nombres',
            'sexo',
            'edad',
            'telefono',
            'estado',
            'cod_estado',
            'municipio',
            'cod_municipio',
            'parroquia',
            'cod_parroquia',
            'nomb_centro',
            'cod_circulo',)

    def calculo_cod_parr(self, obj):
        """ Metodo para arrojar el string de parroquia."""
        id_est = obj.cod_estado
        id_mun = obj.cod_municipio
        id_parr = obj.cod_parroquia
        parroquias = Parroquia.objects.filter(municipio=id_mun,estado_id=id_est,cod_parroquia=id_parr)[0].parroquia
        #print "PARROQUIA: ",parroquias
        return parroquias

    def calculo_cod_mun(self, obj):
        """ Metodo para arrojar el string de municipio."""
        id_est = obj.cod_estado
        id_mun = obj.cod_municipio
        municipios = Municipio.objects.filter(cod_municipio=id_mun,estado_id=id_est)[0].municipio
        #print "Municipios: ",municipios
        return municipios

    def calculo_cod_est(self, obj):
        """ Metodo para arrojar el string de estado."""
        id_est = obj.cod_estado
        estado = Estado.objects.filter(cod_estado=id_est)[0].estado
        #print "estado: ",estado
        return estado

    def calculo_nac(self, obj):
        if obj.nac == 'V':
            nac = 'Venezolano'
        else:
            nac = 'Extrajero'
        return nac

    def calculo_sexo(self, obj):
        if obj.sexo == 'F':
            sexo = 'Femenino'
        if obj.sexo == 'M':
            sexo = 'Masculino'
        return sexo
