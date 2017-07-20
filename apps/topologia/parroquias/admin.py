from django.contrib import admin
from .models import Parroquia


class RetornarParroquia(admin.ModelAdmin):

    list_display = ('estado', 'municipio', 'parroquia')
    search_fields = ('parroquia',)
    ordering = ('estado',)
    fields = ('estado', 'municipio', 'parroquia')

admin.site.register(Parroquia, RetornarParroquia)
