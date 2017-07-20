from django.forms import ModelForm
from django import forms
from apps.topologia.estados.models import Estado

class FormEstado(ModelForm):
    class Meta:
	model = Estado
	exclude = {'user',}
