from django.db import models
from django.contrib.auth.models import User

class BitacoraClp(models.Model):
    """
    Clase para el ingreso de los procesos de la bitacora para los jefes de CLP
    """
    #nac_new = models.CharField(choices=NACIONALIDAD, default='V', max_length=1)
    #nac_old = models.CharField(choices=NACIONALIDAD, default='V', max_length=1)
    cedula_new = models.IntegerField()
    cedula_old = models.IntegerField()
    nombres_new = models.CharField(max_length=50, null=True, blank=True)
    nombres_old = models.CharField(max_length=50, null=True, blank=True)
    sexo_new = models.CharField(max_length=1, blank=True, null=True)
    sexo_old = models.CharField(max_length=1, blank=True, null=True)
    edad_new = models.CharField(max_length=5, null=True, blank=True)
    edad_old = models.CharField(max_length=5, null=True, blank=True)
    tlf_new = models.CharField(max_length=11, null=True, blank=True)
    tlf_old = models.CharField(max_length=11, null=True, blank=True)
    user_update = models.ForeignKey(User, null=True, blank=True, related_name='+')
    fecha_update = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
