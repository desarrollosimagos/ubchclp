# -*- encoding: utf-8 -*-
from django.db import models

# Create your models here.
NACIONALIDAD = (
    ('V', 'Venezolano'),
    ('E', 'Extranjero'),
)
SEXO = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),
)


class Clp(models.Model):
    """ Clase que define todo lo referente a las CLP
    Registrar Modificar Eliminar y Consultar"""

    nac = models.CharField(verbose_name="Nacionalidad", max_length=1, choices=NACIONALIDAD, default='V')
    cedula = models.IntegerField()
    nombres = models.CharField(verbose_name="Nombres", max_length=150)
    sexo = models.CharField(verbose_name="Sexo", max_length=1, choices=SEXO, null=True)
    edad = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    nomb_centro = models.CharField(verbose_name="Nombre Agrupacion", max_length=200)
    cod_estado = models.IntegerField()
    cod_municipio = models.IntegerField()
    cod_parroquia = models.IntegerField()
    cod_circulo = models.IntegerField()


def __unicode__(self):
        # Método para retornar por defecto el valor de un campo especificado
    return self.cedula
