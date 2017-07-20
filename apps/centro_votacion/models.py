# -*- coding: utf-8 -*-
from django.db import models

# Modelo de Topologia / Centro de Votacion

# Clase de estado


class CentroVotacion(models.Model):
    """Esta es la Clase que define todo lo referente a los Centros de Votacion
        Registrar Modificar Eliminar y Consultar
    """
    estado = models.IntegerField(null=True)
    municipio = models.IntegerField(null=True)
    parroquia = models.IntegerField(null=True)
    id_mun = models.IntegerField(null=True)
    cod_n = models.IntegerField(null=True)
    cod_v = models.CharField(max_length=1500, null=True)
    c_votacion = models.TextField(max_length=1500,)
    direccion = models.TextField(max_length=1500,)
    user = models.CharField(max_length=15, null=True)
    date_create = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    date_update = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

    def __unicode__(self):
        return self.c_votacion

    def __str(self):
        return self.c_votacion
