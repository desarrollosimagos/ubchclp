from django.db import models
from django.contrib.auth.models import User


class BitacoraManager(models.Manager):
    def create_bitacora(self,
                        cedula_old,
                        cedula_new,
                        p_nombre_old,
                        s_nombre_old,
                        p_nombre_new,
                        s_nombre_new,
                        p_apellido_old,
                        s_apellido_old,
                        p_apellido_new,
                        s_apellido_new,
                        twitter_old,
                        twitter_new,
                        telefono_old,
                        telefono_new,
                        cod_ubch_old,
                        cod_ubch_new,
                        user_update,
                        ):
        book = self.create(
            cedula_old=cedula_old,
            cedula_new=cedula_new,
            p_nombre_old=p_nombre_old,
            s_nombre_old=s_nombre_old,
            p_nombre_new=p_nombre_new,
            s_nombre_new=s_nombre_new,
            p_apellido_old=p_apellido_old,
            s_apellido_old=s_apellido_old,
            p_apellido_new=p_apellido_new,
            s_apellido_new=s_apellido_new,
            twitter_old=twitter_old,
            twitter_new=twitter_new,
            telefono_old=telefono_old,
            telefono_new=telefono_new,
            cod_ubch_old=cod_ubch_old,
            cod_ubch_new=cod_ubch_new,
            user_update=user_update,
        )

        return book


class Bitacora(models.Model):
    cedula_old = models.IntegerField()
    p_nombre_old = models.CharField(max_length=50,)
    s_nombre_old = models.CharField(max_length=50, null=True, blank=True)
    p_apellido_old = models.CharField(max_length=50,)
    s_apellido_old = models.CharField(max_length=50, null=True, blank=True)
    twitter_old = models.CharField(max_length=50, null=True, blank=True)
    telefono_old = models.CharField(max_length=11,)

    cedula_new = models.IntegerField()
    p_nombre_new = models.CharField(max_length=50,)
    s_nombre_new = models.CharField(max_length=50, null=True, blank=True)
    p_apellido_new = models.CharField(max_length=50,)
    s_apellido_new = models.CharField(max_length=50, null=True, blank=True)
    twitter_new = models.CharField(max_length=50, null=True, blank=True)
    telefono_new = models.CharField(max_length=11,)

    cod_ubch_old = models.IntegerField()
    cod_ubch_new = models.IntegerField()
    #Auditoria
    user_update = models.ForeignKey(User, null=True, blank=True, related_name='+')
    fecha_update = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

    objects = BitacoraManager()
