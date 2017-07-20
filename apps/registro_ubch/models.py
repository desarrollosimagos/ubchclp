from django.db import models


class UnoPorDiez(models.Model):

    cedula = models.IntegerField(unique=True, )
    p_nombre = models.CharField(max_length=50,)
    s_nombre = models.CharField(max_length=50, null=True, blank=True)
    p_apellido = models.CharField(max_length=50,)
    s_apellido = models.CharField(max_length=50, null=True, blank=True)
    cod_ubch = models.IntegerField()
    cedula_jefe = models.IntegerField()
    twitter = models.CharField(max_length=50, null=True, blank=True)
    direcc_p = models.TextField(null=True, blank=True)
    telefono = models.CharField(max_length=11,)
    estado = models.IntegerField(null=True, blank=True)
    municipio = models.IntegerField(null=True, blank=True)
    parroquia = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
            return self.p_nombre
