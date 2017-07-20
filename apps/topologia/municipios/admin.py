from django.contrib import admin
from .models import Municipio


class RetornarMunicipio(admin.ModelAdmin):
    #fields = ['municipio', 'estado']
    list_display = ('estado', 'municipio')
    search_fields = ('municipio',)
    ordering = ('estado',)
    fields = ('estado', 'municipio',)

admin.site.register(Municipio, RetornarMunicipio)
