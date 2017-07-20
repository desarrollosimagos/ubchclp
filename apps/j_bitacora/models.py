from django.db import models
from django.contrib.auth.models import User


class Bitacora(models.Model):

    cedula_old = models.IntegerField()
    nombre_old = models.CharField(max_length=50,)
    telefono_old = models.CharField(max_length=11,)

    cedula_new = models.IntegerField()
    nombre_new = models.CharField(max_length=50,)
    telefono_new = models.CharField(max_length=11,)


    #Auditoria
    user_update = models.ForeignKey(User, null=True, blank=True, related_name='+')
    fecha_update = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
