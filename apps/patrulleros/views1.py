#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

from django.views.generic import CreateView, View
from django.http import HttpResponse
from rest_framework import status, generics
from rest_framework.exceptions import APIException
import json
from .models import Patrullero
from apps.clp.models import Clp
from apps.registro.models import Ubch
from .serializer import PatrulleroSerializer, PatrulleroDatosSerializer
import sys
from django.db import connection
import class_report


class NotFound(APIException):
    """Clase para validar registro no encontrado"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'No se encontraron Registros'

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail


class PatrulleroView(generics.ListAPIView):
    model = Patrullero
    serializer_class = PatrulleroSerializer
    lookup_field = 'cedula_jefe'

    def get_queryset(self):
        cedula_jefe = self.kwargs['cedula_jefe']
        if cedula_jefe is not None:
            queryset = Patrullero.objects.all()
            queryset = queryset.filter(cedula_jefe=cedula_jefe).order_by('id')
            if queryset.exists():
                return queryset
            else:
                raise NotFound()


class PatrulleroDatosView(generics.ListAPIView):
    model = Patrullero
    serializer_class = PatrulleroDatosSerializer
    lookup_field = 'cedula'

    def get_queryset(self):
        cedula = self.kwargs['cedula']
        if cedula is not None:
            queryset = Patrullero.objects.all()
            queryset = queryset.filter(cedula=cedula)
            print queryset
            if queryset.exists():
                return queryset
            else:
                raise NotFound()


class RegistrarPatrullero(CreateView):
    template_name = 'registro/patrullero.html'
    model = Patrullero

    def post(self, request, *args, **kwargs):
        accion = self.request.POST.get('accion')

        response_data = {}
        if accion == 'guardar':
            cedula = self.request.POST.get('cedula')
            cedula_jefe = self.request.POST.get('cedula_jefe')
            existe_clp = Clp.objects.filter(cedula=cedula)
            existe_ubch = Ubch.objects.filter(cedula=cedula)
            existe_clp_pa = Patrullero.objects.filter(cedula=cedula, cedula_jefe=cedula_jefe)
            existe_patru = Patrullero.objects.filter(cedula=cedula)

            if existe_clp.exists():
                response_data['cedula_clp'] = 'existe'
                return HttpResponse(json.dumps(response_data), content_type='application/json')
            elif existe_ubch.exists():
                response_data['cedula_ubch'] = 'existe'
                return HttpResponse(json.dumps(response_data), content_type='application/json')
            elif existe_clp_pa.exists():
                response_data['cedula_clp_pa'] = 'existe'
                return HttpResponse(json.dumps(response_data), content_type='application/json')
            if existe_patru.exists():
                response_data['cedula'] = 'existe'

                cedula_jef = existe_patru.values('cedula_jefe')
                cedua_je = cedula_jef[0]['cedula_jefe']
                queryset_jefe = Ubch.objects.filter(cedula=str(cedua_je))
                nombre_jefe = queryset_jefe.values('nombre')
                response_data['nombre'] = nombre_jefe[0]['nombre']

                return HttpResponse(json.dumps(response_data), content_type='application/json')
            else:
                form_class = self.get_form_class()
                form = self.get_form(form_class)
                add = form.save(commit=False)
                if form.is_valid():
                    direccion = self.request.POST.get('direccion')
                    add.direccion = direccion.upper()
                    add.save()
                    ultimo = add.id
                    response_data['save'] = 'ok'
                    response_data['id'] = ultimo
                    if ultimo is not None:
                        return HttpResponse(json.dumps(response_data), content_type='application/json')
                    else:
                        response_data['save'] = 'error'
                        return HttpResponse(json.dumps(response_data), content_type='application/json')
                else:
                    return HttpResponse('2')
        elif accion == 'buscar':

            response_data = []
            cedula_jefe = self.request.POST.get('cedula')
            queryset = Patrullero.objects.filter(cedula_jefe=cedula_jefe)
            queryset = queryset.values('id', 'cedula', 'p_nombre', 's_nombre', 'p_apellido', 's_apellido', 'telefono', 'twitter', 'agregado', 'direccion').order_by('id')

            tam = len(queryset)
            i = 0
            while i < tam:
                response_data.append(queryset[i])
                i += 1

            data = json.dumps(response_data)

            return HttpResponse(data, content_type='application/json')
        else:
            id_reg = self.request.POST.get('id_reg')
            Patrullero.objects.filter(id=id_reg).delete()
            existe = Patrullero.objects.filter(id=id_reg).exists()
            if existe is False:
                response_data['delete'] = 'ok'
                data = HttpResponse(json.dumps(response_data),
                                    content_type='application/json'
                                    )
                return data

from django.conf import settings


# Clase para la generacion de los reportes del patrullero

class PatrulleroReport(View):

    template_name = 'registro/patrullero.html'
    model = Patrullero

    def get_context_data(self, **kwargs):
        context = {}
        return context

    def get(self, request, *args, **kwargs):

        reload(sys)

        sys.setdefaultencoding("utf-8")
        cedula = kwargs.get('cedula', None)
        pdf = class_report.PDF(orientation='L',
                               unit='mm',
                               format='letter'
                               )

        pdf.set_author('Marcel Arcuri')
        pdf.alias_nb_pages()  # LLAMADA DE PAGINACION
        pdf.add_page()  # AÑADE UNA NUEVA PAGINACION
        pdf.set_fill_color(157, 188, 201)  # COLOR DE BORDE DE LA CELDA
        pdf.set_text_color(24, 29, 31)  # COLOR DEL TEXTO
        pdf.set_margins(10, 10, 10)

        cursor = connection.cursor()

        sql_ced = "SELECT  r.cod_ubch, r.nom_ubch, r.cedula, r.nombre AS nombres, r.telefono, r.cargo,"
        sql_ced += "(select estado from estados_estado  where cod_estado =r.cod_estado) AS estado,"
        sql_ced += "(select municipio from municipios_municipio AS m  where estado_id =r.cod_estado AND cod_municipio =r.cod_municipio) AS municipio,"
        sql_ced += "(select parroquia from parroquias_parroquia AS p  where estado_id =r.cod_estado AND municipio =r.cod_municipio AND cod_parroquia = r.cod_parroquia) AS parroquia"
        sql_ced += " FROM registro_ubch r"
        sql_ced += " WHERE r.cedula = %s"

        cursor.execute(sql_ced, [cedula])

        row = dictfetchall(cursor)
        cedula = row[0]['cedula']
        nombre = row[0]['nombres']
        telefono = row[0]['telefono']
        cargo = row[0]['cargo']
        cod_ubch = row[0]['cod_ubch']
        cv = row[0]['nom_ubch']
        estado = row[0]['estado']
        municipio = row[0]['municipio']
        parroquia = row[0]['parroquia']

        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(27, 128, 172)
        pdf.cell(250, 5, 'Datos del Jefe del Patrulla', '', 1, 'C', 0)
        pdf.ln()

        pdf.set_text_color(0, 0, 0)

        pdf.set_x(50)
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
        pdf.cell(20, 5, '0'+str(telefono).decode("UTF-8"), 0, 1)
        pdf.ln()

        pdf.set_x(50)
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(10, 5, 'Cargo:'.decode("UTF-8"), 0, 0)
        pdf.set_font('Arial', '', 8)
        pdf.cell(20, 5, str(cargo).decode("UTF-8"), 0, 1)
        pdf.ln()

        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(27, 128, 172)
        pdf.cell(250, 5, 'Datos de la UBCH', '', 1, 'C', 0)
        pdf.ln()

        pdf.set_text_color(0, 0, 0)
        pdf.set_x(50)
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(16, 5, 'Estado: ', 0, 0)
        pdf.cell(16, 5, str(estado).upper().decode("UTF-8"), 0, 0)
        pdf.cell(16, 5, 'Municipio:   '+str(municipio).upper().decode("UTF-8"), 0, 0)
        pdf.ln(5);
        pdf.set_x(50)
        pdf.cell(32, 5, 'Parroquia:   '+str(parroquia).upper().decode("UTF-8"), 0, 0)
        pdf.ln(5)
        pdf.set_x(50)
        pdf.cell(12, 5, 'Código:'.decode("UTF-8"), 0, 0)
        pdf.set_font('Arial', '', 8)
        pdf.cell(15, 5, str(cod_ubch).decode("UTF-8"), 0, 0)

        pdf.set_font('Arial', 'B', 8)
        pdf.cell(12, 5, 'Centro:'.decode("UTF-8"), 0, 0)
        pdf.set_font('Arial', '', 8)
        pdf.cell(150, 5, str(cv).decode("UTF-8"), 0, 1)
        pdf.ln()

        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(27, 128, 172)
        pdf.cell(250, 5, 'Listado de Patrulleros', '', 1, 'C', 0)
        pdf.ln()

        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', 'B', 8)  # Fuente de la Letra
        pdf.set_fill_color(217, 237, 247)
        pdf.cell(10, 5, 'Nº'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
        pdf.cell(18, 5, 'Cédula'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
        pdf.cell(69, 5, 'Nombre'.decode("UTF-8"), 'LTRB', 0, 'L', 1)
        pdf.cell(20, 5, 'Teléfono'.decode("UTF-8"), 'LTRB', 0, 'L', 1)
        pdf.cell(15, 5, 'Tipo'.decode("UTF-8"), 'LTRB', 0, 'L', 1)
        pdf.cell(128, 5, 'Dirección'.decode("UTF-8"), 'LTRB', 1, 'L', 1)
        pdf.set_font('Arial', '', 8)  # Fuente de la Letra

        sql = "SELECT cedula, COALESCE(p_nombre,'') ||' '|| COALESCE(s_nombre,'') ||' '|| COALESCE(p_apellido,'') ||' '|| COALESCE(s_apellido,'') as nombres, COALESCE(telefono, '') as telefono, COALESCE(direccion,'') as direccion, agregado"
        sql += " FROM patrulleros_patrullero WHERE cedula_jefe=%s ORDER BY id"

        cursor.execute(sql, [cedula])

        row = dictfetchall(cursor)
        pdf.set_fill_color(255, 255, 255)
        i = 1
        j = 0
        for ubch in row:
            pdf.set_text_color(0, 0, 0)
            resto = i % 2
            agre = ''
            count_dir = len(ubch['direccion'])
            print "COUNT: ",count_dir

            if int(count_dir) > 161:
                j = 10
            elif int(count_dir) > 156:
                j = 10
            elif int(count_dir) > 144:
                j = 10
            elif int(count_dir) >= 98:
                j = 5
            else:
                j = 0

            if ubch['agregado'] == True:
                agre = 'Agregado'
                pdf.set_text_color(5, 109, 43)
            else:
                agre = 'Principal'

            if resto == 0:
                pdf.set_fill_color(239, 239, 239)
            pdf.cell(10, 5 + j, str(i), 'LTRB', 0, 'C', 1)
            pdf.cell(18, 5 + j, str(ubch['cedula']), 'LRTB', 0, 'R', 1)
            pdf.cell(69, 5 + j, str(ubch['nombres']), 'LRTB', 0, 'L', 1)
            pdf.cell(20, 5 + j, str(ubch['telefono']), 'LTRB', 0, 'R', 1)
            pdf.cell(15, 5 + j, str(agre), 'LTRB', 0, 'C', 1)
            pdf.multi_cell(128, 5, str(ubch['direccion']).decode("UTF-8"), 1, 'J', 1)

            i += 1
            pdf.set_fill_color(255, 255, 255)

        self.get_context_data()
        arch = 'patrullero'
        ruta_reporte = settings.MEDIA_PDF
        archivo = ruta_reporte+'/'+str(cedula)+'.pdf'
        pdf.output(archivo, 'F')
        archivo = open(archivo, "r")
        response = HttpResponse(archivo.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="'+str(arch)+'.pdf"'

        return response


class ReportePatrullero(CreateView):
    template_name = 'registro/reportejefes.html'
    model = Patrullero

    def post(self, request, *args, **kwargs):
        #accion = self.request.POST.get('accion')
        codigo_clp = self.request.POST.get('cedula_jefe')

        sql = "SELECT  cod_ubch, nom_ubch, cedula, nombre, telefono, cargo "
        sql += "FROM registro_ubch WHERE cedula=%s"
        cursor = connection.cursor()

        cursor.execute(sql, [codigo_clp])

        row = dictfetchall(cursor)
        data = json.dumps(row)
        return HttpResponse(data)


def dictfetchall(cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]



