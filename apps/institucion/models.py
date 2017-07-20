from django.db import models


class Institucion(models.Model):

    institucion = models.TextField()
    cedula_representante = models.IntegerField(unique=True, )
    nombre = models.CharField(max_length=50,)
    telefono = models.CharField(max_length=11,)

