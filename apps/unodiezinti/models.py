from django.contrib.auth.models import User
from django.db import models
from apps.datos.models import Datos


class UnoDiezInti(models.Model):
    datos = models.ForeignKey(Datos, on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL,  null=True)

