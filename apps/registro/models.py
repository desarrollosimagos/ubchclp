# -*- encoding: utf-8 -*-
from django.db import models

# Create your models here.
NACIONALIDAD = (
    ('V', 'Venezolano'),
    ('E', 'Extranjero'),
)


class Ubch(models.Model):
    """ Clase que define todo lo referente a las UBCH
    Registrar Modificar Eliminar y Consultar """

    cod_estado = models.IntegerField()
    cod_municipio = models.IntegerField(null=True)
    cod_parroquia = models.IntegerField(null=True)
    cod_ubch = models.IntegerField()
    nom_ubch = models.CharField(max_length=200)
    nac = models.CharField(verbose_name="Nacionalidad", max_length=1, choices=NACIONALIDAD, default='V')
    cedula = models.CharField(verbose_name="Cédula", max_length=12, unique=True, null=True)
    nombre = models.CharField(verbose_name="Nombres", max_length=200, null=True)
    telefono = models.CharField(max_length=50)
    cod_cargo = models.IntegerField()
    cargo = models.CharField(max_length=200)


def __unicode__(self):
        """ Método para retornar por defecto el valor de un campo especificado """
        return self.cedula
