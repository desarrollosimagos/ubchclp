from rest_framework.serializers import ModelSerializer
from .models import Parroquia


class ParroquiaSerializer(ModelSerializer):
    class Meta:
        model = Parroquia
        fields = ('id', 'parroquia', 'municipio', 'estado')

    def __unicode__(self):
        return self.parroquia
