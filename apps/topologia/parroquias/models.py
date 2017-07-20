from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from ..estados.models import Estado
from ..municipios.models import Municipio


class Parroquia(models.Model):
	"""Esta es la Clase que define todo lo referente a los parroquias
		Registrar Modificar Eliminar y Consultar
	"""
	parroquia     = models.CharField(max_length=50)
	estado        = models.ForeignKey(Estado, to_field='cod_estado', on_delete=models.SET_NULL, related_name='estado_parroquia', null=True)
	cod_parroquia = models.IntegerField(null=True)
	municipio     = models.IntegerField(null=True)
	user          = models.CharField(max_length=15, null=True)
	date_create   = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	date_update   = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

	def __unicode__(self):
		return self.parroquia

	def __str__(self):
		return self.parroquia
