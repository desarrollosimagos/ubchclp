from apps.patrulleros.models import Patrullero
from rest_framework import serializers


class PatrulleroSerializer(serializers.ModelSerializer):

    # Metodo para validar campo null p_apellido
    def null_p_apellido(self, obj):
        p_apellido = ""
        if unicode(obj.p_apellido) == 'None':
            p_apellido = ""
        else:
            p_apellido = unicode(obj.p_apellido)
        return p_apellido

    # Metodo para validar campo null s_apellido
    def null_s_apellido(self, obj):
        s_apellido = ""
        if unicode(obj.s_apellido) == 'None':
            s_apellido = ""
        else:
            s_apellido = unicode(obj.s_apellido)
        return s_apellido

    # Metodo para validar campo null p_nombre
    def null_p_nombre(self, obj):
        p_nombre = ""
        if unicode(obj.p_nombre) == 'None':
            p_nombre = ""
        else:
            p_nombre = unicode(obj.p_nombre)
        return p_nombre

    # Metodo para validar campo null null_s_nombre
    def null_s_nombre(self, obj):
        s_nombre = ""
        if unicode(obj.s_nombre) == 'None':
            s_nombre = ""
        else:
            s_nombre = unicode(obj.s_nombre)
        return s_nombre

    def null_s_twitter(self, obj):
        twitter = ""
        if unicode(obj.twitter) == 'None':
            twitter = ""
        else:
            twitter = unicode(obj.twitter)
        return twitter

    def es_agregado(self, obj):
        agre = 'Agregado'
        if obj.agregado is False:
            agre = ''
        return agre

    p_apellido = serializers.SerializerMethodField('null_p_apellido')  # Metodo para validar campo null p_apellido
    s_apellido = serializers.SerializerMethodField('null_s_apellido')  # Metodo para validar campo null s_apellido
    p_nombre = serializers.SerializerMethodField('null_p_nombre')  # Metodo para validar campo null p_nombre
    s_nombre = serializers.SerializerMethodField('null_s_nombre')
    twitter = serializers.SerializerMethodField('null_s_twitter')
    agregado = serializers.SerializerMethodField('es_agregado')

    class Meta:
        model = Patrullero
        fields = (
            'id',
            'cedula',
            'p_apellido',
            's_apellido',
            'p_nombre',
            's_nombre',
            'telefono',
            'twitter',
            'agregado',
            'direccion',
            )


class PatrulleroDatosSerializer(serializers.ModelSerializer):

    # Metodo para validar campo null p_apellido
    def null_p_apellido(self, obj):
        p_apellido = ""
        if unicode(obj.p_apellido) == 'None':
            p_apellido = ""
        else:
            p_apellido = unicode(obj.p_apellido)
        return p_apellido

    # Metodo para validar campo null s_apellido
    def null_s_apellido(self, obj):
        s_apellido = ""
        if unicode(obj.s_apellido) == 'None':
            s_apellido = ""
        else:
            s_apellido = unicode(obj.s_apellido)
        return s_apellido

    # Metodo para validar campo null p_nombre
    def null_p_nombre(self, obj):
        p_nombre = ""
        if unicode(obj.p_nombre) == 'None':
            p_nombre = ""
        else:
            p_nombre = unicode(obj.p_nombre)
        return p_nombre

    # Metodo para validar campo null null_s_nombre
    def null_s_nombre(self, obj):
        s_nombre = ""
        if unicode(obj.s_nombre) == 'None':
            s_nombre = ""
        else:
            s_nombre = unicode(obj.s_nombre)
        return s_nombre

    def null_s_twitter(self, obj):
        twitter = ""
        if unicode(obj.twitter) == 'None':
            twitter = ""
        else:
            twitter = unicode(obj.twitter)
        return twitter

    def es_agregado(self, obj):
        agre = 'Agregado'
        if obj.agregado is False:
            agre = ''
        return agre

    p_apellido = serializers.SerializerMethodField('null_p_apellido')  # Metodo para validar campo null p_apellido
    s_apellido = serializers.SerializerMethodField('null_s_apellido')  # Metodo para validar campo null s_apellido
    p_nombre = serializers.SerializerMethodField('null_p_nombre')  # Metodo para validar campo null p_nombre
    s_nombre = serializers.SerializerMethodField('null_s_nombre')
    twitter = serializers.SerializerMethodField('null_s_twitter')
    agregado = serializers.SerializerMethodField('es_agregado')

    class Meta:
        model = Patrullero
        fields = (
            'id',
            'cedula',
            'p_apellido',
            's_apellido',
            'p_nombre',
            's_nombre',
            'telefono',
            'twitter',
            'agregado',
            'direccion',
            )
