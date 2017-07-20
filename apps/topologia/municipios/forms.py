from django.forms import ModelForm
from django import forms
from apps.topologia.municipios.models import Municipio

class FormMunicipio(ModelForm):
    class Meta:
	model = Municipio
	exclude = {'user',}
