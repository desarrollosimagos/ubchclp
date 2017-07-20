from django.views.generic import ListView
from .models import Clp
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
import csv
import os
from django.core import serializers
from apps.clp.serializer import ClpSerializer


class ListarView(ListView):

    template_name = 'clp/listar.html'
    model = Clp
    paginate_by = 20
    context_object_name = 'listar_clp'

    class Meta:
        ordering = ["cedula"]


@login_required(login_url='/')
def load_data(request):
    """ Funcion que permite importar data CSV."""
    os.path.dirname(os.path.abspath(__file__))

    DIR_URL = os.getcwd()

    reader = csv.reader(open(DIR_URL+str("/apps/clp/script/jefes_clp_aragua.csv")))

    # Recorrido de los registros
    for row in reader:
        data = row[0].split(';')
        jefes = Clp(
            nac=data[0],
            cedula=data[1],
            nombres=data[2],
            sexo=data[3],
            edad=data[4],
            telefono=data[5],
            nomb_centro=data[6],
            cod_estado=data[7],
            cod_municipio=data[8],
            cod_parroquia=data[9],
            cod_circulo=data[10],)

        jefes.save()
    return HttpResponseRedirect('/clp/listar')

##############################################################################
#             Clase para capturar datos serializados con viewsets
##############################################################################

from rest_framework import generics, status
from rest_framework.exceptions import APIException


class NotFound(APIException):
    """ Clase para validar registro no encontrado."""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'No se encontraron Registros'

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail


class ListarClpCedula(generics.ListAPIView):
    """ Generacion de la api."""
    model = Clp
    serializer_class = ClpSerializer
    lookup_field = 'cedula'

    def get_queryset(self):
        cedula = self.kwargs['cedula']
        if cedula is not None:
            queryset = Clp.objects.all()
            queryset = queryset.filter(cedula=cedula)

            if queryset.exists():

                return queryset
            else:
                raise NotFound()


class ListarClpCodigo(generics.ListAPIView):
    """ Generacion de la api."""
    model = Clp
    serializer_class = ClpSerializer
    lookup_field = 'codigo'

    def get_queryset(self):
        codigo = self.kwargs['codigo']

        if codigo is not None:
            queryset = Clp.objects.all()
            queryset = queryset.filter(cod_circulo=codigo)

            if queryset.exists():

                return queryset
            else:
                raise NotFound()


def BuscarAjaxCentros(request):

    id_est = request.GET['id_est']
    id_mun = request.GET['id_mun']
    id_parr = request.GET['id_parr']
    jefes = Clp.objects.filter(estado_id=id_est, municipio=id_mun, parroquia=id_parr)
    data = serializers.serialize('json', jefes, fields=(''))
    return HttpResponse(data, content_type='application/json')
