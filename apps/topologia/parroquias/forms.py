from django.forms import ModelForm
from django import forms
from apps.topologia.parroquias.models import Parroquia

class FormParroquia(ModelForm):
    class Meta:
        model = Parroquia
        exclude = {'user',}
