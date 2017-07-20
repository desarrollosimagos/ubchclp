from django.db import models
from ..estados.models import Estado


class Municipio(models.Model):
    municipio     = models.CharField(verbose_name="Municipio", max_length=50)
    cod_municipio = models.IntegerField(null=True)
    estado        = models.ForeignKey(Estado, to_field='cod_estado', on_delete=models.SET_NULL, related_name='estado_municipio', null=True) # Clave unica que hace referencia a estado a traves de cod_estado con clave unica (unique)
    user          = models.CharField(max_length=15, null=True)
    date_create   = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    date_update   = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

    def __unicode__(self):
        return self.municipio
