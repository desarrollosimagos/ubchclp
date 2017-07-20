#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-
"""
Libreria FPDF python
"""

import class_report
####################################################


from django.views.generic import CreateView, View, DetailView, DeleteView
from .models import ClpUBC
from apps.clp.models import Clp
from apps.registro.models import Ubch
from apps.j_bitacora.models import Bitacora
from apps.c_bitacora.models import BitacoraClp
from apps.patrulleros.models import Patrullero
from serializer import ClpUbchSerializer
from django.http import HttpResponse
from rest_framework import status, generics
from rest_framework.exceptions import APIException
import json
from django.core import serializers
import sys
import os
from django.db import connection


class NotFound(APIException):
    """Clase para validar registro no encontrado"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'No se encontraron Registrosss'

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail



class ListarClpCedula(DetailView):
    """ Generacion de la api."""
    model = Clp
    
    def get(self, request, *args, **kwargs):
        
        cedula = self.request.GET.get('cedula')
        response_data = {}
        estatus = 200
        if cedula is not None:
            queryset = Clp.objects.all()
            queryset = queryset.filter(cedula=cedula)
            
            if queryset.exists():

                queryset = queryset.values('nombres','cod_circulo')
                data = {}
                for value in queryset:
                    data = value
                
                cod_circulo = queryset[0]['cod_circulo']
                
                queryset_ubch = ClpUBC.objects.all()
                queryset_ubch_f = queryset_ubch.filter(cod_circulo=cod_circulo)
                
                cod_ubch = queryset_ubch_f.values_list('cod_ubch')

                queryset = Ubch.objects.all()
                queryset = queryset.filter(cod_ubch__in=cod_ubch, cod_cargo=1)
                
                datos = queryset.values('cod_ubch', 'nom_ubch', 'cedula', 'nombre', 'telefono')
                
                if queryset_ubch_f.exists():
                    dato = []
                    for value in datos:
                        
                        ubch_id = queryset_ubch.filter(cod_ubch=value['cod_ubch']).values('id')
                       
                        data_id = {}
                        for value_id in ubch_id:
                            data_id = value_id

                        value.update(data_id)

                        dato.append(value)
                    response_data['ubch'] = dato
                else:
                    response_data['ubch'] = 'error'
                response_data['clp'] = data
            else:
                estatus = 404

        return HttpResponse(json.dumps(response_data), status=estatus, content_type='application/json')



class UbchSearchView(DetailView):
    """ Clase que permite generar la Api"""
    model = Ubch
    
    def get(self, request, *args, **kwargs):
        estatus = 200
        response_data = {}
        cod_ubch = self.request.GET.get('cod_ubch')
        if cod_ubch is not None:
            
            queryset = Ubch.objects.all()
            queryset = queryset.filter(cod_ubch=cod_ubch, cod_cargo=1)
            if queryset.exists():
                
                queryset = queryset.values('nom_ubch', 'cedula', 'nombre', 'telefono')
                data = {}
                for value in queryset:
                    data = value
                
                response_data['ubch'] = data
        
            else:
                estatus = 404
        else:
            estatus = 404

        return HttpResponse(json.dumps(response_data), status=estatus, content_type='application/json')


class RegistroClpUbch(CreateView):
    template_name = 'registro/clp_ubch.html'
    model = ClpUBC

    def post(self, request, *args, **kwargs):
        accion = self.request.POST.get('accion')
        
        response_data = {}
        estatus = 200
        cod_ubch = self.request.POST.get('cod_ubch')
        cod_circulo = self.request.POST.get('cod_circulo')
        query_clp = ClpUBC.objects.filter(cod_ubch=cod_ubch, cod_circulo=cod_circulo)
        query_ubch = ClpUBC.objects.filter(cod_ubch=cod_ubch)
        
        if query_clp.exists():
            response_data['ubch_clp'] = 'existe'
        elif query_ubch.exists():
            response_data['ubch'] = 'existe'
            
            cod_cir = query_ubch.values('cod_circulo')
            
            queryset_clp1 = Clp.objects.filter(cod_circulo=cod_cir)
            jefe_circulo = queryset_clp1.values('nombres')
            data = {}
            for value in jefe_circulo:
                data = value
            response_data['jefe'] = data
        else:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            add = form.save(commit=False)
            if form.is_valid():
                add.save()
                ultimo = add.cod_ubch
                response_data['save'] = 'ok'
                response_data['id'] = ultimo

        return HttpResponse(json.dumps(response_data), status=estatus, content_type='application/json')
        

class DeleteClpUbchView(DeleteView):
    model = ClpUBC

    def delete(self, request, *args, **kwargs):
        
        response_data = {}
        existe = ClpUBC.objects.filter(id=self.kwargs['pk'])
        if existe.exists():
            self.object = self.get_object()
            self.object.delete()
            response_data['eliminar'] = 'ok'
            return HttpResponse(json.dumps(response_data), status=200, content_type='application/json')


class UbchView(generics.ListAPIView):
    model = ClpUBC
    lookup_field = 'cod_ubch'

    def get_queryset(self):

        cod_ubch = self.kwargs['cod_ubch']
        if cod_ubch is not None:
            queryset = ClpUBC.objects.all()
            queryset = queryset.filter(cod_ubch=cod_ubch)
            if queryset.exists():
                return queryset
            else:
                raise NotFound()


class ClpUbchView(generics.ListAPIView):
    model = ClpUBC
    serializer_class = ClpUbchSerializer
    #lookup_field = 'cod_clp'

    def get_queryset(self):
        cod_clp = self.kwargs['cod_clp']
        #cod_clp = self.request.QUERY_PARAMS.get('cod_clp', None)
        print self.request.QUERY_PARAMS
        if cod_clp is not None:
            queryset = ClpUBC.objects.all()
            queryset = queryset.filter(cod_circulo=cod_clp)
            if queryset.exists():
                return queryset
            else:
                raise NotFound()


def dictfetchall(cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]


from django.conf import settings


class ClpUbchReport(View):

    template_name = 'registro/clp_ubch.html'

    def get_context_data(self, **kwargs):
        context = {}
        return context

    def get(self, request, *args, **kwargs):

        reload(sys)
        sys.setdefaultencoding("utf-8")
        cod_circulo = kwargs.get('cod_circulo', None)

        pdf = class_report.ClpUbchReportG(orientation='P',
                                          unit='mm',
                                          format='letter'
                                          )

        pdf.set_author('Marcel Arcuri')
        pdf.alias_nb_pages()  # LLAMADA DE PAGINACION
        pdf.add_page()  # AÑADE UNA NUEVA PAGINACION
        pdf.set_fill_color(157, 188, 201)  # COLOR DE BORDE DE LA CELDA
        pdf.set_text_color(24, 29, 31)  # COLOR DEL TEXTO
        pdf.set_margins(10, 10, 10)

        pdf.set_font('Arial', 'B', 12)
        pdf.set_fill_color(217, 237, 247)
        pdf.cell(195, 5, 'SISTEMA DE REGISTRO Y CONSULTA DE CLP/UBCH/1x10', '', 1, 'C', 1)
        pdf.ln(10)

        cursor = connection.cursor()

        sql_clp = "SELECT cedula, nombres,telefono, nomb_centro FROM clp_clp WHERE cod_circulo=%s;"

        cursor.execute(sql_clp, [cod_circulo])

        row = dictfetchall(cursor)

        cedula = row[0]['cedula']
        nombre = row[0]['nombres']
        telefono = row[0]['telefono']
        cv = row[0]['nomb_centro']

        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(27, 128, 172)
        pdf.cell(190, 5, 'Datos del Jefe del CLP', '', 1, 'C', 0)
        pdf.ln()

        pdf.set_text_color(0, 0, 0)

        pdf.set_font('Arial', 'B', 8)
        pdf.cell(11, 5, 'Cédula:'.decode("UTF-8"), 0, 0)

        pdf.set_font('Arial', '', 8)
        pdf.cell(15, 5, str(cedula), 0, 0)

        pdf.set_font('Arial', 'B', 8)
        pdf.cell(13, 5, 'Nombre:', 0, 0)
        pdf.set_font('Arial', '', 8)
        pdf.cell(90, 5, str(nombre).decode("UTF-8"), 0, 0)

        pdf.set_font('Arial', 'B', 8)
        pdf.cell(15, 5, 'Teléfono:'.decode("UTF-8"), 0, 0)
        pdf.set_font('Arial', '', 8)
        pdf.cell(20, 5, str(telefono).decode("UTF-8"), 0, 1)
        pdf.ln()

        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(27, 128, 172)
        pdf.cell(190, 5, 'Datos del CLP', '', 1, 'C', 0)
        pdf.ln()

        pdf.set_text_color(0, 0, 0)

        pdf.set_font('Arial', 'B', 8)
        pdf.cell(12, 5, 'Código:'.decode("UTF-8"), 0, 0)
        pdf.set_font('Arial', '', 8)
        pdf.cell(15, 5, str(cod_circulo).decode("UTF-8"), 0, 0)

        pdf.set_font('Arial', 'B', 8)
        pdf.cell(12, 5, 'Centro:'.decode("UTF-8"), 0, 0)
        pdf.set_font('Arial', '', 8)
        pdf.cell(150, 5, str(cv).decode("UTF-8"), 0, 1)
        pdf.ln()

        pdf.ln()

        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', 'B', 9)  # Fuente de la Letra
        pdf.set_fill_color(217, 237, 247)
        pdf.cell(10, 5, 'Nº'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
        pdf.cell(25, 5, 'Codigo UBC', 'LTRB', 0, 'L', 1)
        pdf.cell(160, 5, 'Nombre UBCH', 'LTRB', 1, 'L', 1)
        pdf.set_font('Arial', '', 9)  # Fuente de la Letra

        sql = "SELECT  ubch.cod_ubch, ubch.nom_ubch FROM clp_ubch_clpubc as cu"
        sql += " INNER JOIN registro_ubch as ubch on cu.cod_ubch=ubch.cod_ubch"
        sql += " WHERE cod_circulo=%s"
        sql += " GROUP BY ubch.cod_ubch,ubch.nom_ubch;"

        cursor.execute(sql, [cod_circulo])

        row = dictfetchall(cursor)
        pdf.set_fill_color(255, 255, 255)
        i = 1
        for ubch in row:
            resto = i % 2
            if resto == 0:
                pdf.set_fill_color(239, 239, 239)
            pdf.cell(10, 5, str(i), 'LTRB', 0, 'C', 1)
            pdf.cell(25, 5, str(ubch['cod_ubch']), 'LRTB', 0, 'L', 1)
            pdf.cell(160, 5, str(ubch['nom_ubch']), 'LTRB', 1, 'L', 1)
            i += 1
            pdf.set_fill_color(255, 255, 255)

        self.get_context_data()
        ruta_reporte = settings.MEDIA_PDF
        archivo = ruta_reporte+'/'+str(cod_circulo)+'.pdf'
        pdf.output(archivo, 'F')
        archivo = open(archivo, "r")
        response = HttpResponse(archivo.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="'+str(archivo)+'.pdf"'

        return response


class ReporteClpUbch(CreateView):
    template_name = 'registro/reporteubchclp.html'
    model = ClpUBC

    def post(self, request, *args, **kwargs):
        #accion = self.request.POST.get('accion')
        codigo_clp = self.request.POST.get('codigo_clp')

        sql = "SELECT cedula, nombres,telefono, nomb_centro FROM clp_clp WHERE cod_circulo=%s;"

        cursor = connection.cursor()

        cursor.execute(sql, [codigo_clp])

        row = dictfetchall(cursor)
        data = json.dumps(row)
        return HttpResponse(data)
