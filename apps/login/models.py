from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Usuarios(models.Model):
	user        = models.OneToOneField(User)
	tlf         = models.CharField(max_length=15)
	user_accion = models.CharField(max_length=15, null=True)

	def __unicode__(self):
		return self.user.username
