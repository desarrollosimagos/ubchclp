from django.views.generic import ListView
from .models import Ubch
from django.http import HttpResponse, HttpResponseRedirect
import csv
import os
from django.core import serializers
from apps.registro.serializer import UbchSerializer, UbchListSerializer


class ListarView(ListView):
    """ Vista basada en clase: (`Listar`)

    :param template_name: ruta de la plantilla
    :param model: Modelo al cual se hace referencia
    :param context_object_name: nombre del objeto que contiene esta vista
    :param paginate_by: Genera la paginacion de los registros en base a la cantidad definida.
    """
    template_name = 'ubch/listar.html'
    model = Ubch
    paginate_by = 20
    context_object_name = 'listar_ubch'




def load_data(request):
    """Funcion que permite importar data csv."""
    os.path.dirname(os.path.abspath(__file__))

    DIR_URL = os.getcwd()

    reader = csv.reader(open(DIR_URL+str("/apps/registro/script/ubch.csv")))

    # Recorrido de los registros
    for row in reader:
        data = row[0].split(';')
        centro = Ubch(
            cod_estado=data[1],
            cod_municipio=data[3],
            cod_parroquia=data[5],
            nom_ubch=data[7],
            cod_ubch=data[6],
            cedula=data[9],
            nombre=data[10],
            telefono=data[11],
            cod_cargo=data[12],
            cargo=data[13],
            nac=data[8],)
        centro.save()
    return HttpResponseRedirect('/ubch/listar')

##############################################################################
#             Clase para capturar datos serializados con viewsets
##############################################################################

from rest_framework import generics, status
from rest_framework.exceptions import APIException


class NotFound(APIException):
    """Clase para validar registro no encontrado"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'No se encontraron Registros'

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail


class RegistroView(generics.ListAPIView):
    """ Clase que permite generar la Api"""
    model = Ubch
    serializer_class = UbchSerializer
    #lookup_field = 'cedula'
    lookup_field = ('cedula')
    #filter_backends = (filters.DjangoFilterBackend,)
    #filter_fields = ('cedula')

    def get_queryset(self):

        cedula = self.kwargs['cedula']
        #cod_ubch = self.kwargs['cod_ubch']
        #print cod_ubch
        if cedula is not None:
            queryset = Ubch.objects.all()
            queryset = queryset.filter(cedula=cedula)

            if queryset.exists():

                return queryset
            else:
                raise NotFound()


class UbchListView(generics.ListAPIView):
    """ Clase que permite generar la Api"""
    model = Ubch
    serializer_class = UbchListSerializer
    lookup_field = 'cod_ubch'

    def get_queryset(self):

        cod_ubch = self.kwargs['cod_ubch']
        if cod_ubch is not None:
            queryset = Ubch.objects.all()
            queryset = queryset.filter(cod_ubch=cod_ubch, cod_cargo=1)
            if queryset.exists():

                return queryset
            else:
                raise NotFound()


def BuscarAjaxCentros(request):

    id_est = request.GET['id_est']
    id_mun = request.GET['id_mun']
    id_parr = request.GET['id_parr']
    centros = Ubch.objects.filter(estado_id=id_est, municipio=id_mun,
                                  parroquia=id_parr
                                  )
    data = serializers.serialize('json', centros, fields=(''))
    return HttpResponse(data, content_type='application/json')
