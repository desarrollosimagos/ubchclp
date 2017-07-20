from django.views.generic import ListView
from .models import Bitacora
from django.http import HttpResponse, HttpResponseRedirect
import csv
import os


class BitacoraView(ListView):
    """ Vista basada en clase: (`Template de buscador de bitacora (procesos)`)

    :param template_name: ruta de la plantilla
    :param model: Modelo al cual se hace referencia
    """
    template_name = 'bitacora/search_bitacora.html'
    model = Bitacora
