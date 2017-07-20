from django.db import models


class ClpUBC(models.Model):

    cod_circulo = models.IntegerField()
    cod_ubch = models.IntegerField()

    def __unicode__(self):
            return self.cod_circulo
