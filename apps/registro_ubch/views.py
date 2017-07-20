#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
from django.views.generic import CreateView, View, ListView, DetailView, DeleteView
from apps.clp.models import Clp
from apps.registro.models import Ubch
from apps.institucion.models import Institucion
from apps.patrulleros.models import Patrullero
from apps.registro_ubch.models import UnoPorDiez
from apps.registro_ubch.serializer import UnoPorDiezSerializer
from apps.p_bitacora.models import Bitacora
from django.http import HttpResponse
from rest_framework import status, generics
from rest_framework.exceptions import APIException
import json
import sys
from django.db import connection
import class_report


class NotFound(APIException):
    """Clase para validar registro no encontrado"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'No se encontraron Registros'

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail



class UnoDiezView(DetailView):
    model = Patrullero

    def get(self, request, *args, **kwargs):

        cedula = self.request.GET.get('cedula')

        if cedula is not None:
            response_data = {}
            estatus = 200

            queryset = Patrullero.objects.all()
            queryset_u = UnoPorDiez.objects.all()
            queryset_ub = Ubch.objects.all()

            queryset_f = queryset.filter(cedula=cedula)

            if queryset_f.exists():

                queryset_v = queryset_f.values('p_nombre', 's_nombre', 'p_apellido','s_apellido', 'telefono', 'twitter')

                data = {}
                for value in queryset_v:
                    data = value
                response_data['patrullero'] = data

                queryset_u_f = queryset_u.filter(cedula_jefe=cedula)

                if queryset_u_f.exists():
                    queryset_u_v = queryset_u_f.values('id', 'cedula', 'p_nombre', 's_nombre', 'p_apellido', 's_apellido', 'telefono', 'direcc_p', 'cod_ubch').order_by('id')

                    dato = []
                    for value in queryset_u_v:

                        nomb_ubch = queryset_ub.filter(cod_ubch=value['cod_ubch']).values('nom_ubch')
                        data_nomb = {}
                        for value_id in nomb_ubch:
                            data_nomb = value_id

                        value.update(data_nomb)

                        dato.append(value)

                    response_data['unodiez'] = dato
                else:
                    response_data['ubch'] = 'error'
                return HttpResponse(json.dumps(response_data), status=estatus, content_type='application/json')
            else:
                return HttpResponse(status=404)


class Listar1X10(ListView):
    template_name = 'registro/listar1x10.html'
    model = UnoPorDiez

    def get_context_data(self, **kwargs):
        context = super(Listar1X10, self).get_context_data(**kwargs)
        cedula_jefe = self.kwargs['cedula']

        patrullero = Patrullero.objects.all()
        patrullero = patrullero.filter(cedula=cedula_jefe)
        patrullero = patrullero.values(
            'cedula',
            'p_nombre',
            's_nombre',
            'p_apellido',
            's_apellido',
            'telefono',
            'direccion')
        context['patrullero'] = patrullero

        queryset = UnoPorDiez.objects.all()
        queryset = queryset.filter(cedula_jefe=cedula_jefe)
        print queryset.query
        context['listado'] = queryset
        return context


class UnoPorDiezView(generics.ListAPIView):
    model = UnoPorDiez
    serializer_class = UnoPorDiezSerializer
    lookup_field = 'cedula_patrullero'

    def get_queryset(self):

        cedula_jefe = self.kwargs['cedula_patrullero']
        if cedula_jefe is not None:
            queryset = UnoPorDiez.objects.all()
            queryset = queryset.filter(cedula_jefe=cedula_jefe)
            if queryset.exists():
                return queryset
            else:
                raise NotFound()


# Registro uno por diez

class RegistrarUnoPorDiez(CreateView):
    template_name = 'registro/registro.html'
    model = UnoPorDiez

    def post(self, request, *args, **kwargs):
        accion = self.request.POST.get('accion')
        # print "REggg: ",self.request.POST
        response_data = {}
        if accion == 'guardar':
            cedula_jefe = self.request.POST.get('cedula_jefe')
            cedula = self.request.POST.get('cedula')
            tipo_registro = self.request.POST.get('tipo')
            if tipo_registro == 'institucion':
                cedula_jefe = self.request.POST.get('cedula_represe')
                nombre = self.request.POST.get('nombre_represe')
                telefono = self.request.POST.get('telefono_represe')
                institucion = self.request.POST.get('institucion')
                
                obj_institucion = Institucion.objects
                if obj_institucion.exists() is False:
                    
                    obj_institucion.create(cedula_representante=cedula_jefe,
                                               nombre=nombre,
                                               telefono=telefono,
                                               institucion=institucion)
                
                form_class = self.get_form_class()
                form = self.get_form(form_class)
                add = form.save(commit=False)
                if form.is_valid():

                    direcc_p = self.request.POST.get('direcc_p')
                    add.direcc_p = direcc_p.upper()

                    add.save()
                    ultimo = add.id
                    response_data['save'] = 'ok'
                    response_data['id'] = ultimo
                    return HttpResponse(json.dumps(response_data),
                                        content_type='application/json')
                else:
                    return HttpResponse('2')
            else:
                existe_clp = Clp.objects.filter(cedula=cedula)
                existe_ubch = Ubch.objects.filter(cedula=cedula)
                existe_patru = Patrullero.objects.filter(cedula=cedula)
                existe_institu = Institucion.objects.filter(cedula_representante=cedula)

                existe_patr = UnoPorDiez.objects.all()
                existe_patr = existe_patr.filter(cedula=cedula,
                                                 cedula_jefe=cedula_jefe)
                existe_uno = UnoPorDiez.objects.filter(cedula=cedula)

                if existe_clp.exists():
                    response_data['cedula_clp'] = 'existe'
                    return HttpResponse(json.dumps(response_data),
                                        content_type='application/json')
                elif existe_ubch.exists():
                    response_data['cedula_ubch'] = 'existe'
                    return HttpResponse(json.dumps(response_data),
                                        content_type='application/json')
                elif existe_patru.exists():
                    response_data['cedula_patrullero'] = 'existe'
                    return HttpResponse(json.dumps(response_data),
                                        content_type='application/json')
                elif existe_patr.exists():
                    response_data['cedula_patr'] = 'existe'
                    return HttpResponse(json.dumps(response_data),
                                        content_type='application/json')
                elif existe_institu.exists():
                    response_data['cedula_inst'] = 'existe'
                    return HttpResponse(json.dumps(response_data),
                                        content_type='application/json')
                elif existe_uno.exists():
                    response_data['cedula'] = 'existe'

                    cedula_jef = existe_uno.values('cedula_jefe')

                    cedula_je = cedula_jef[0]['cedula_jefe']
                    queryset_patru = Patrullero.objects.filter(
                        cedula=str(cedula_je))
                    queryset_clp_sear = Clp.objects.filter(cedula=str(cedula_je))
                    queryset_ubch_sear = Ubch.objects.filter(cedula=str(cedula_je))
                    if len(queryset_patru) > 0:
                        
                        cedula = queryset_patru.values('cedula')[0]['cedula']
                        p_nombre = queryset_patru.values('p_nombre')[0]['p_nombre']

                        s_nombre = queryset_patru.values('s_nombre')[0]['s_nombre']

                        p_apellido = queryset_patru.values('p_apellido')
                        p_apellido = p_apellido[0]['p_apellido']

                        s_apellido = queryset_patru.values('s_apellido')
                        s_apellido = s_apellido[0]['s_apellido']

                        if s_nombre is None:
                            s_nombre = ''
                        if s_apellido is None:
                            s_apellido = ''

                        nombre = str(p_nombre) + ' ' + str(unicode(s_nombre)) + ' '+ str(p_apellido) + ' '+ str(unicode(s_apellido))
                        
                        response_data['pertenece'] = 'patrullero'
                        response_data['cedula_pa'] = cedula
                    elif len(queryset_clp_sear) > 0:
                        nombre = queryset_clp_sear.values('nombres')[0]['nombres']
                        response_data['pertenece'] = 'clp'
                    elif len(queryset_ubch_sear) > 0:
                        nombre = queryset_ubch_sear.values('nombre')[0]['nombre']
                        response_data['pertenece'] = 'ubch'

                    response_data['nombre'] = nombre

                    return HttpResponse(json.dumps(response_data),
                                        content_type='application/json')
                else:
                    form_class = self.get_form_class()
                    form = self.get_form(form_class)
                    add = form.save(commit=False)
                    if form.is_valid():

                        direcc_p = self.request.POST.get('direcc_p')
                        add.direcc_p = direcc_p.upper()

                        add.save()
                        ultimo = add.id
                        response_data['save'] = 'ok'
                        response_data['id'] = ultimo
                        return HttpResponse(json.dumps(response_data),
                                            content_type='application/json')
                    else:
                        return HttpResponse('2')
        elif accion == 'update':

            cedula_jefe = self.request.POST.get('cedula_jefe')
            cedula_jefe_m = self.request.POST.get('cedula_jefe_m')

            user = request.user

            que_unox10 = UnoPorDiez.objects.all()
            que_unox10_fil = que_unox10.filter(cedula_jefe=cedula_jefe)
            que_unox10_fil.update(cedula_jefe=cedula_jefe_m)

            total = que_unox10.filter(cedula_jefe=cedula_jefe_m).count()
            if total > 0:
                pat = Patrullero.objects.all()
                pat_old = pat.filter(cedula=cedula_jefe)
                # valores = ['p_nombre', 's_nombre', 'p_apellido']
                pat_old_v = pat_old.values('p_nombre',
                                           's_nombre',
                                           'p_apellido',
                                           's_apellido',
                                           'twitter',
                                           'telefono',
                                           'cod_ubch_p'
                                           )

                pat_new = pat.filter(cedula=cedula_jefe_m)
                pat_new_v = pat_new.values('p_nombre',
                                           's_nombre',
                                           'p_apellido',
                                           's_apellido',
                                           'twitter',
                                           'telefono',
                                           'cod_ubch_p'
                                           )

                p_nombre_ol = pat_old_v[0]['p_nombre']
                s_nombre_ol = pat_old_v[0]['s_nombre']
                if s_nombre_ol is None:
                    s_nombre_ol = ''
                p_apellido_ol = pat_old_v[0]['p_apellido']
                s_apellido_ol = pat_old_v[0]['s_apellido']
                if s_apellido_ol is None:
                    s_apellido_ol = ''

                twitter_ol = pat_old_v[0]['twitter']
                telefono_ol = pat_old_v[0]['telefono']

                p_nombre_ne = pat_new_v[0]['p_nombre']
                s_nombre_ne = pat_new_v[0]['s_nombre']
                p_apellido_ne = pat_new_v[0]['p_apellido']
                s_apellido_ne = pat_new_v[0]['s_apellido']
                twitter_ne = pat_new_v[0]['twitter']
                telefono_ne = pat_new_v[0]['telefono']

                cod_ubch_ol = pat_old_v[0]['cod_ubch_p']
                cod_ubch_ne = pat_new_v[0]['cod_ubch_p']

                Bitacora.objects.create_bitacora(
                   cedula_jefe,
                   cedula_jefe_m,
                   p_nombre_ol,
                   s_nombre_ol,
                   p_nombre_ne,
                   s_nombre_ne,
                   p_apellido_ol,
                   p_apellido_ne,
                   s_apellido_ol,
                   s_apellido_ne,
                   twitter_ol,
                   twitter_ne,
                   telefono_ol,
                   telefono_ne,
                   cod_ubch_ol,
                   cod_ubch_ne,
                   user,
                )
                response_data['update'] = 'ok'
                return HttpResponse(json.dumps(response_data),
                                    content_type='application/json')
        elif accion == 'buscar':
            response_data = []
            cedula_jefe = self.request.POST.get('cedula')
            queryset = Patrullero.objects.filter(cedula=cedula_jefe)
            queryset = queryset.values('p_nombre',
                                       's_nombre',
                                       'p_apellido',
                                       's_apellido',
                                       'telefono',
                                       'twitter'
                                       )

            tam = len(queryset)
            i = 0
            while i < tam:
                response_data.append(queryset[i])
                i += 1
            if len(response_data) > 0:
                data = json.dumps(response_data)
                return HttpResponse(data, content_type='application/json')
            else:
                response_dat = {}
                response_dat['existe'] = 'no'
                data = json.dumps(response_dat)
                return HttpResponse(data, content_type='application/json')

        elif accion == 'buscar_uno':
            # print "ACCION: ",accion
            response_data = []
            response_dat = {}
            cedula_jefe = self.request.POST.get('cedula')

            queryset = UnoPorDiez.objects.filter(cedula_jefe=cedula_jefe)
            
            for record in queryset:
                # queryset_ub = Ubch.objects.filter(cod_ubch=record.cod_ubch).distinct('nom_ubch')
                # for ubch_record in queryset_ub:
                #     nom_ubch =  ubch_record.nom_ubch
                    
                queryset_ub = Ubch.objects.filter(cod_ubch=record.cod_ubch).values('nom_ubch').distinct()
                for ubch_record in queryset_ub:
                    nom_ubch =  ubch_record['nom_ubch']
                    
                if unicode(record.s_nombre) == 'None':
                    segundo_n = ''
                else:
                    segundo_n = record.s_nombre
                
                if unicode(record.s_apellido) == 'None':
                    segundo_a = ''
                else:
                    segundo_a = record.s_apellido               
                
                nombres = unicode(record.p_nombre)+' ' + unicode(segundo_n)+' '+unicode(record.p_apellido)+' '+unicode(segundo_a)
                json_obj = dict(id=record.id,
                                cedula = record.cedula,
                                nombres = nombres,
                                telefono = record.telefono,
                                twitter = record.twitter,
                                estado = record.estado,
                                municipio = record.municipio,
                                parroquia = record.parroquia,
                                direcc_p = record.direcc_p,
                                cod_ubch = record.cod_ubch,
                                cedula_jefe = record.cedula_jefe,
                                nom_ubch = nom_ubch
                                )
           
                response_data.append(json_obj)
            data = json.dumps(response_data)
            
            return HttpResponse(data, content_type='application/json')
        
        elif accion == 'buscar_represe':
            
            response_data = {}
            cedula_jefe = self.request.POST.get('cedula')
            queryset = Institucion.objects.filter(cedula_representante=cedula_jefe)
            
            queryset_clp = Clp.objects.filter(cedula=cedula_jefe)
            queryset_ubch = Ubch.objects.filter(cedula=cedula_jefe)
            queryset_patru = Patrullero.objects.filter(cedula=cedula_jefe)
            queryset_unodiez = UnoPorDiez.objects.filter(cedula=cedula_jefe)
            
            if queryset_clp.exists():
                response_data['existe_clp'] = 'si'
            elif queryset_ubch.exists():
                response_data['existe_ubch'] = 'si'
            elif queryset_patru.exists():
                response_data['existe_patru'] = 'si'
            elif queryset_unodiez.exists():
                response_data['existe_unodiez'] = 'si'
            elif queryset.exists():
                queryset = queryset.values('nombre',  'telefono', 'institucion')
                for value in queryset:
                    response_data = value
            else:                
                response_data['existe'] = 'no'
            
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            id_reg = self.request.POST.get('id_reg')
            UnoPorDiez.objects.filter(id=id_reg).delete()
            existe = UnoPorDiez.objects.filter(id=id_reg).exists()
            if existe is False:
                response_data['delete'] = 'ok'
                data = HttpResponse(json.dumps(response_data),
                                    content_type='application/json'
                                    )
                return data


class DeleteUnoPorDiez(DeleteView):
    model = UnoPorDiez
    def delete(self, request, *args, **kwargs):
        response_data = {}
        existe = UnoPorDiez.objects.filter(id=self.kwargs['pk'])
        if existe.exists():
            print 'dsfdf'
            self.object = self.get_object()
            self.object.delete()
            response_data['eliminar'] = 'ok'
            return HttpResponse(json.dumps(response_data), status=200, content_type='application/json')

class RegistrarUnoPorJefeInst(CreateView):
    template_name = 'registro/registrojefesinstituciones.html'
    model = UnoPorDiez

    def post(self, request, *args, **kwargs):
        accion = self.request.POST.get('accion')

        if accion == 'buscar_jefes':
            cedula = self.request.POST.get('cedula')
            queryset_clp = Clp.objects.all()
            queryset_ubch = Ubch.objects.all()

            queryset_clp = queryset_clp.filter(cedula=cedula)
            queryset_ubch = queryset_ubch.filter(cedula=cedula)

            response_data = {}
            data_existe = 'si'
            cod_cargo = 0
            if queryset_clp.exists():
                # data =  queryset_clp.values('nombres','telefono')
                nombre = queryset_clp.values('nombres')[0]['nombres']
                telefono = queryset_clp.values('telefono')[0]['telefono']
                codigo = queryset_clp.values('cod_circulo')[0]['cod_circulo']
                centro = queryset_clp.values('nomb_centro')[0]['nomb_centro']
            elif queryset_ubch.exists():
                nombre = queryset_ubch.values('nombre')[0]['nombre']
                telefono = queryset_ubch.values('telefono')[0]['telefono']
                codigo = queryset_ubch.values('cod_ubch')[0]['cod_ubch']
                centro = queryset_ubch.values('nom_ubch')[0]['nom_ubch']
                cod_cargo = queryset_ubch.values('cod_cargo')[0]['cod_cargo']
            else:
                data_existe = 'no'

            if data_existe == 'si':
                response_data['nombre'] = nombre
                response_data['telefono'] = telefono
                response_data['codigo'] = codigo
                response_data['centro'] = centro
                response_data['cod_cargo'] = cod_cargo
            else:
                response_data['existe'] = data_existe

            return HttpResponse(json.dumps(response_data),
                                content_type='application/json')

from django.conf import settings

# Clase para Reportes


class Lista1x10Report(View):

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
      
        sql_ced = "SELECT p.cedula,COALESCE(p.p_nombre,'') ||' '||COALESCE(p.s_nombre,'') ||' '||COALESCE(p.p_apellido,'')||' '||COALESCE(p.s_apellido,'') AS nombres,"
        sql_ced += "p.twitter,p.telefono,"
        sql_ced += "p.direccion,"
        sql_ced += "p.agregado,"
        sql_ced += "r.cedula AS cedula_jefe,"
        sql_ced += "r.nombre AS nombre_jefe,"
        sql_ced += "r.telefono AS telefono_jefe,"
        sql_ced += "COALESCE((SELECT estado FROM estados_estado WHERE cod_estado=p.estado),'') AS estado,"
        sql_ced += "COALESCE((SELECT municipio FROM municipios_municipio WHERE estado_id=p.estado AND cod_municipio=p.municipio),'') AS municipio,"
        sql_ced += "COALESCE((SELECT parroquia FROM parroquias_parroquia WHERE estado_id=p.estado AND municipio=p.municipio AND cod_parroquia=p.parroquia),'') AS parroquia"
        sql_ced += " FROM patrulleros_patrullero AS p"
        sql_ced += " INNER JOIN registro_ubch AS r  ON p.cedula_jefe=r.cedula::integer"
        sql_ced += " WHERE p.cedula=%s"

        cursor.execute(sql_ced, [cedula])

        row = dictfetchall(cursor)
        cedula = row[0]['cedula']
        nombre = row[0]['nombres']
        telefono = row[0]['telefono']
        direccion = row[0]['direccion']
        agregado = row[0]['agregado']
        cedula_jefe = row[0]['cedula_jefe']
        nombre_jefe = row[0]['nombre_jefe']
        telefono_jefe = row[0]['telefono_jefe']
        estado = row[0]['estado']
        municipio = row[0]['municipio']
        parroquia = row[0]['parroquia']

        agre = ''
        if agregado is True:
            agre = 'Agregado'
        else:
            agre = "Principal"

        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(27, 128, 172)
        pdf.cell(190, 5, 'Datos del Patrullero', '', 1, 'C', 0)
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
        pdf.cell(14, 5, 'Teléfono:'.decode("UTF-8"), 0, 0)
        pdf.set_font('Arial', '', 8)
        pdf.cell(20, 5, str(telefono).decode("UTF-8"), 0, 0)

        pdf.set_font('Arial', 'B', 8)
        pdf.cell(8, 5, 'Tipo:', 0, 0)
        pdf.set_font('Arial', '', 8)
        pdf.cell(15, 5, str(agre).decode("UTF-8"), 0, 1)

        pdf.cell(16, 5, 'Estado: ', 0, 0)
        pdf.cell(16, 5, str(estado).decode("UTF-8"), 0, 0)
        pdf.cell(16, 5, 'Municipio:   ' + str(municipio).decode("UTF-8"), 0, 0)

        pdf.ln(5)
        pdf.cell(32, 5, 'Parroquia:   ' + str(parroquia).decode("UTF-8"), 0, 0)
        pdf.ln(5)

        pdf.set_font('Arial', 'B', 8)
        pdf.cell(16, 5, 'Dirección:'.decode("UTF-8"), 0, 0)
        pdf.set_font('Arial', '', 8)
        pdf.multi_cell(250, 5, str(direccion).decode("UTF-8"), 0, 1)
        pdf.ln(10)

        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(27, 128, 172)
        pdf.cell(190, 5, 'Datos del Jefe de UBCH', '', 1, 'C', 0)
        pdf.ln()

        pdf.set_text_color(0, 0, 0)

        pdf.set_font('Arial', 'B', 8)
        pdf.cell(12, 5, 'Cédula:'.decode("UTF-8"), 0, 0)
        pdf.set_font('Arial', '', 8)
        pdf.cell(15, 5, str(cedula_jefe).decode("UTF-8"), 0, 0)

        pdf.set_font('Arial', 'B', 8)
        pdf.cell(12, 5, 'Nombre:'.decode("UTF-8"), 0, 0)
        pdf.set_font('Arial', '', 8)
        pdf.cell(90, 5, str(nombre_jefe).decode("UTF-8"), 0, 0)

        pdf.set_font('Arial', 'B', 8)
        pdf.cell(14, 5, 'Teléfono:'.decode("UTF-8"), 0, 0)
        pdf.set_font('Arial', '', 8)
        pdf.cell(20, 5, str(telefono_jefe).decode("UTF-8"), 0, 0)

        pdf.ln(15)

        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(27, 128, 172)
        pdf.cell(190, 5, 'Listado 1X10', '', 1, 'C', 0)
        pdf.ln()

        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', 'B', 10)  # Fuente de la Letra
        pdf.set_fill_color(217, 237, 247)
        pdf.cell(10, 5, 'Nº'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
        pdf.cell(18, 5, 'Cédula'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
        pdf.cell(95, 5, 'Nombre'.decode("UTF-8"), 'LTRB', 0, 'L', 1)
        pdf.cell(25, 5, 'Teléfono'.decode("UTF-8"), 'LTRB', 0, 'L', 1)
        pdf.cell(110, 5, 'Dirección'.decode("UTF-8"), 'LTRB', 1, 'L', 1)

        pdf.set_font('Arial', '', 9)  # Fuente de la Letra

        sql = "SELECT cedula,COALESCE(p_nombre,'') ||' '||COALESCE(s_nombre,'') ||' '||COALESCE(p_apellido,'')||' '||COALESCE(s_apellido,'') AS nombres,telefono, COALESCE(direcc_p,'') AS direcc_p"
        sql += " FROM registro_ubch_unopordiez WHERE cedula_jefe=%s"

        cursor.execute(sql, [cedula])

        row = dictfetchall(cursor)
        pdf.set_fill_color(255, 255, 255)
        i = 1
        j = 0
        for ubch in row:
            resto = i % 2
            count_d = 0
            if resto == 0:
                pdf.set_fill_color(239, 239, 239)
            if ubch['direcc_p'] is not None:
                count_d = len(ubch['direcc_p'])

            if int(count_d) > 127:
                j = 10
            elif int(count_d) > 64:
                j = 5
            else:
                j = 0

            pdf.set_font('Arial', '', 8)  # Fuente de la Letra
            pdf.cell(10, 5 + j, str(i), 'LTRB', 0, 'C', 1)
            pdf.cell(18, 5 + j, str(ubch['cedula']), 'LRTB', 0, 'R', 1)
            pdf.cell(95, 5 + j, str(ubch['nombres']), 'LRTB', 0, 'L', 1)
            pdf.cell(25, 5 + j, str(ubch['telefono']), 'LTRB', 0, 'R', 1)
            pdf.multi_cell(110, 5, str(ubch['direcc_p']).decode("UTF-8"), 1, 'J', 1)

            i += 1
            pdf.set_fill_color(255, 255, 255)

        self.get_context_data()
        ruta_reporte = settings.MEDIA_PDF
        archivo = ruta_reporte + '/' + str(cedula) + '.pdf'
        pdf.output(archivo, 'F')
        archivo = open(archivo, "r")
        response = HttpResponse(archivo.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="' + str(archivo) + '.pdf"'

        return response


class Reporte1x10(CreateView):
    template_name = 'registro/reporte1x10.html'
    model = Patrullero


class Lista1x10ubchReport(ListView):
    """
     Clase para la generacion de listado de 1x10 por ubch (s)
    """

    # template_name = 'registro/reporte1x10_ubch.html'
    # model = Patrullero

    def get_context_data(self, **kwargs):
        context = {}
        return context

    def get(self, request, *args, **kwargs):

        reload(sys)

        sys.setdefaultencoding("utf-8")
        todos = kwargs.get('tipo', None)
       

        # ============================================================================
        #                 INICIO REPORTE DE LISTADO DE 1X10 POR UBCH
        # ============================================================================
        # Instancia de la clase heredada L es horizontal y P es vertical

        pdf = class_report.Ubch1X10ReportE(orientation='L', unit='mm', format='letter') #HORIENTACION DE LA PAGINA

        pdf.set_author('Marcel Arcuri y Jesus laya')
        pdf.alias_nb_pages()  # LLAMADA DE PAGINACION
        pdf.add_page()  # ANADE UNA NUEVA PAGINACION
        pdf.set_margins(10, 10, 10)  # MARGENE DEL DOCUMENTO
        
        tamano = 133
        tamano1 = 100
                
        if todos == "todos":
            # Ejecucion de la consulta de listado 1x10 por ubch
            cursor = connection.cursor()

            sql = "SELECT "
            sql += "r_ubch.cod_ubch AS codigo, "
            sql += "r_ubch.nom_ubch AS nom_ubch, "
            sql += "COUNT (r.id) AS cantidad"
            sql += " FROM registro_ubch_unopordiez AS r"
            sql += " INNER JOIN patrulleros_patrullero AS p ON p.cedula = r.cedula_jefe"
            sql += " INNER JOIN registro_ubch AS r_ubch ON r_ubch.cedula::integer = p.cedula_jefe"
            sql += " GROUP BY r_ubch.cod_ubch, r_ubch.nom_ubch"
            cursor.execute(sql)
            row = dictfetchall(cursor)
            # print "LISTADO DE 1x10 POR UBCH: ",row

            pdf.set_font('Arial','B',10)
            pdf.ln(5)
            pdf.set_fill_color(0,0,0)
            pdf.set_text_color(255,255,255)
            pdf.cell(253,10,"CANTIDAD DE 1X10 POR UBCH",'LR',1,'C',1)
            pdf.ln(5)

            # Fila de la cabezara de la tabla
            pdf.set_fill_color(0,121,194)
            pdf.set_text_color(255,255,255)
            pdf.cell(8,8,"N°".decode("UTF-8"),'LTBR',0,'C',1)
            pdf.cell(18,8,"Código".decode("UTF-8"),'LTBR',0,'C',1)
            pdf.cell(90,8,"Ubch".decode("UTF-8"),'LTBR',0,'C',1)
            pdf.cell(17,8,"Céd / jefe".decode("UTF-8"),'LTBR',0,'C',1)
            pdf.cell(80,8,"Nombre del jefe".decode("UTF-8"),'LTBR',0,'C',1)
            pdf.cell(20,8,"Teléfono".decode("UTF-8"),'LTBR',0,'C',1)
            pdf.cell(20,8,"Cantidad".decode("UTF-8"),'LTBR',1,'C',1)
            pdf.set_fill_color(255,255,255)
            item = 0

            a = 0
            c = 0
            total = 0
            for u in row:

                if a == 15:
                    pdf.add_page()
                    pdf.set_font('Arial','B',10)
                    pdf.ln(5)
                    pdf.set_fill_color(0,0,0)
                    pdf.set_text_color(255,255,255)
                    pdf.cell(253,10,"CANTIDAD DE 1X10 POR UBCH",'LR',1,'C',1)
                    pdf.ln(5)

                    # Fila de la cabezara de la tabla
                    pdf.set_fill_color(0,121,194)
                    pdf.set_text_color(255,255,255)
                    pdf.cell(8,8,"N°".decode("UTF-8"),'LTBR',0,'C',1)
                    pdf.cell(18,8,"Código".decode("UTF-8"),'LTBR',0,'C',1)
                    pdf.cell(90,8,"Ubch".decode("UTF-8"),'LTBR',0,'C',1)
                    pdf.cell(17,8,"Céd / jefe".decode("UTF-8"),'LTBR',0,'C',1)
                    pdf.cell(80,8,"Nombre del jefe".decode("UTF-8"),'LTBR',0,'C',1)
                    pdf.cell(20,8,"Teléfono".decode("UTF-8"),'LTBR',0,'C',1)
                    pdf.cell(20,8,"Cantidad".decode("UTF-8"),'LTBR',1,'C',1)
                    pdf.set_fill_color(255,255,255)
                    c = 0
                    a = 0

                ubch = u['nom_ubch']
                # ubch_can = len(ubch)
                sql_nombre = "SELECT cedula,nombre,telefono FROM registro_ubch WHERE cod_ubch = "+str(u['codigo'])+" and cod_cargo = 1"
                
                cursor.execute(sql_nombre)

                row1 = dictfetchall(cursor)
                nombre = row1[0]['nombre']
                cedula = row1[0]['cedula']
                tlf = row1[0]['telefono']
                cantidad = u['cantidad']
                # nombre_can = len(nombre)
                
                
                sql_tot_jefe = "SELECT COUNT(id)::int  AS tot_jefe FROM registro_ubch_unopordiez WHERE cedula_jefe="+cedula
                
                cursor.execute(sql_tot_jefe)
                row2 = dictfetchall(cursor)
                tot_jefe = row2[0]['tot_jefe']
                
                if tlf == "":
                    tlf = "N/A"
                else:
                    tlf = tlf
                tot_ubch = cantidad + tot_jefe
                
                item = int(item) + 1
                # Filas que vienen de la BD
                pdf.set_font('Arial','B',8)
                pdf.set_fill_color(255,255,255)
                pdf.set_text_color(24,29,31)
                pdf.set_y(38+c)
                pdf.set_x(10)
                pdf.cell(8,10,str(item).decode("UTF-8"),'LTBR',0,'C',1)
                pdf.cell(18,10,str(u['codigo']),'LTBR',0,'C',1)
                pdf.multi_cell(90,5,ubch.decode("UTF-8"),'LTR','J',1)
                pdf.set_y(38+c)
                pdf.set_x(126)
                pdf.cell(17,10,cedula,'LTBR',0,'C',1)
                pdf.multi_cell(80,5,nombre.decode("UTF-8"),'LTR','J',1)
                pdf.set_y(38+c)
                pdf.set_x(223)
                pdf.cell(20,10,str(tlf),'LTBR',0,'C',1)
                pdf.cell(20,10,str(tot_ubch),'LTBR',1,'C',1)
                pdf.cell(250,0.1,'','T',1,'C',1)

                pdf.set_fill_color(255,255,255)
                pdf.set_font('Arial','B',8)

                c = c + 10
                a = a + 1
                total += tot_ubch
        elif todos == "clp":

            cursor = connection.cursor()

            sql = "SELECT "
            sql += "clp.cedula, clp.nombres, clp.telefono, "
            sql += "clp.nomb_centro, clp.cod_circulo, COUNT(ru.cedula) tot_clp "
            sql += " FROM clp_clp AS clp"
            sql += " INNER JOIN registro_ubch_unopordiez AS ru ON clp.cedula=ru.cedula_jefe"
            sql += " GROUP BY clp.cedula, clp.nombres, clp.telefono, clp.nomb_centro, clp.cod_circulo,clp.id"
            sql += " ORDER BY clp.id"
            cursor.execute(sql)
            row = dictfetchall(cursor)
            tot_clp = row[0]['tot_clp']

            pdf.set_font('Arial','B',10)
            pdf.ln(5)
            pdf.set_fill_color(0,0,0)
            pdf.set_text_color(255,255,255)
            pdf.cell(253,10,"CANTIDAD DE 1X10 POR CLP",'LR',1,'C',1)
            pdf.ln(5)

            # Fila de la cabezara de la tabla
            pdf.set_fill_color(0,121,194)
            pdf.set_text_color(255,255,255)
            pdf.cell(8,8,"N°".decode("UTF-8"),'LTBR',0,'C',1)
            pdf.cell(18,8,"Código".decode("UTF-8"),'LTBR',0,'C',1)
            pdf.cell(90,8,"CLP".decode("UTF-8"),'LTBR',0,'C',1)
            pdf.cell(17,8,"Céd / jefe".decode("UTF-8"),'LTBR',0,'C',1)
            pdf.cell(80,8,"Nombre del jefe".decode("UTF-8"),'LTBR',0,'C',1)
            pdf.cell(20,8,"Teléfono".decode("UTF-8"),'LTBR',0,'C',1)
            pdf.cell(20,8,"Cantidad".decode("UTF-8"),'LTBR',1,'C',1)
            pdf.set_fill_color(255,255,255)

            a = 0
            c = 0
            total = 0
            item = 0
            for u in row:

                if a == 15:
                    pdf.add_page()
                    pdf.set_font('Arial','B',10)
                    pdf.ln(5)
                    pdf.set_fill_color(0,0,0)
                    pdf.set_text_color(255,255,255)
                    pdf.cell(253,10,"CANTIDAD DE 1X10 POR CLP",'LR',1,'C',1)
                    pdf.ln(5)

                    # Fila de la cabezara de la tabla
                    pdf.set_fill_color(0,121,194)
                    pdf.set_text_color(255,255,255)
                    pdf.cell(8,8,"N°".decode("UTF-8"),'LTBR',0,'C',1)
                    pdf.cell(18,8,"Código".decode("UTF-8"),'LTBR',0,'C',1)
                    pdf.cell(90,8,"CLP".decode("UTF-8"),'LTBR',0,'C',1)
                    pdf.cell(17,8,"Céd / jefe".decode("UTF-8"),'LTBR',0,'C',1)
                    pdf.cell(80,8,"Nombre del jefe".decode("UTF-8"),'LTBR',0,'C',1)
                    pdf.cell(20,8,"Teléfono".decode("UTF-8"),'LTBR',0,'C',1)
                    pdf.cell(20,8,"Cantidad".decode("UTF-8"),'LTBR',1,'C',1)
                    pdf.set_fill_color(255,255,255)

                    a = 0
                    c = 0
                
                item = int(item) + 1

                pdf.set_font('Arial','B',8)
                pdf.set_fill_color(255,255,255)
                pdf.set_text_color(24,29,31)
                pdf.set_y(38+c)
                pdf.set_x(10)
                pdf.cell(8,10,str(item).decode("UTF-8"),'LTBR',0,'C',1)
                pdf.cell(18,10,str(u['cod_circulo']),'LTBR',0,'C',1)
                pdf.multi_cell(90,5,(u['nomb_centro']).decode("UTF-8"),'LTR','J',1)
                pdf.set_y(38+c)
                pdf.set_x(126)
                pdf.cell(17,10,str(u['cedula']),'LTBR',0,'C',1)
                pdf.multi_cell(80,5,str(u['nombres']).decode("UTF-8"),'LTR','J',1)
                pdf.set_y(38+c)
                pdf.set_x(223)
                pdf.cell(20,10,str(u['telefono']),'LTBR',0,'C',1)
                pdf.cell(20,10,str(u['tot_clp']),'LTBR',1,'C',1)
                pdf.cell(250,0.1,'','T',1,'C',1)

                pdf.set_fill_color(255,255,255)
                pdf.set_font('Arial','B',8)

                c = c + 10
                a = a + 1
                total += tot_clp

        elif todos == "inst":

            cursor = connection.cursor()

            sql = "SELECT "
            sql += "ins.institucion, ins.cedula_representante, "
            sql += "ins.nombre, ins.telefono, COUNT(ru.cedula) tot_ins "
            sql += " FROM institucion_institucion AS ins"
            sql += " INNER JOIN  registro_ubch_unopordiez AS ru ON ins.cedula_representante=ru.cedula_jefe"
            sql += " GROUP BY ins.institucion, ins.cedula_representante, ins.nombre, ins.telefono,ins.id"
            sql += " ORDER BY ins.id;"
            cursor.execute(sql)
            row = dictfetchall(cursor)
            tot_ins = row[0]['tot_ins']

            pdf.set_font('Arial','B',10)
            pdf.ln(5)
            pdf.set_fill_color(0,0,0)
            pdf.set_text_color(255,255,255)
            pdf.cell(253,10,"CANTIDAD DE 1X10 POR INSTITUCIONES",'LR',1,'C',1)
            pdf.ln(5)

            # Fila de la cabezara de la tabla
            pdf.set_fill_color(0,121,194)
            pdf.set_text_color(255,255,255)
            pdf.cell(8,8,"N°".decode("UTF-8"),'LTBR',0,'C',1)
            pdf.cell(100,8,"Institución".decode("UTF-8"),'LTBR',0,'C',1)
            pdf.cell(20,8,"Céd / jefe".decode("UTF-8"),'LTBR',0,'C',1)
            pdf.cell(85,8,"Nombre del jefe".decode("UTF-8"),'LTBR',0,'C',1)
            pdf.cell(20,8,"Teléfono".decode("UTF-8"),'LTBR',0,'C',1)
            pdf.cell(20,8,"Cantidad".decode("UTF-8"),'LTBR',1,'C',1)
            pdf.set_fill_color(255,255,255)

            a = 0
            c = 0
            total = 0
            item = 0
            for u in row:
                if a == 15:
                    pdf.add_page()
                    pdf.set_font('Arial','B',10)
                    pdf.ln(5)
                    pdf.set_fill_color(0,0,0)
                    pdf.set_text_color(255,255,255)
                    pdf.cell(253,10,"CANTIDAD DE 1X10 POR INSTITUCIONES",'LR',1,'C',1)
                    pdf.ln(5)
        
                    # Fila de la cabezara de la tabla
                    pdf.set_fill_color(0,121,194)
                    pdf.set_text_color(255,255,255)
                    pdf.cell(8,8,"N°".decode("UTF-8"),'LTBR',0,'C',1)
                    pdf.cell(100,8,"Institución".decode("UTF-8"),'LTBR',0,'C',1)
                    pdf.cell(20,8,"Céd / jefe".decode("UTF-8"),'LTBR',0,'C',1)
                    pdf.cell(85,8,"Nombre del jefe".decode("UTF-8"),'LTBR',0,'C',1)
                    pdf.cell(20,8,"Teléfono".decode("UTF-8"),'LTBR',0,'C',1)
                    pdf.cell(20,8,"Cantidad".decode("UTF-8"),'LTBR',1,'C',1)
                    pdf.set_fill_color(255,255,255)
                
                    a = 0
                    c = 0
                
                item = int(item) + 1

                pdf.set_font('Arial','B',8)
                pdf.set_fill_color(255,255,255)
                pdf.set_text_color(24,29,31)
                pdf.set_y(38+c)
                pdf.set_x(10)
                pdf.cell(8,10,str(item).decode("UTF-8"),'LTBR',0,'C',1)
                pdf.multi_cell(100,5,(u['institucion']).decode("UTF-8"),'LTR','J',1)
                pdf.set_y(38+c)
                pdf.set_x(118)
                pdf.cell(20,10,str(u['cedula_representante']),'LTBR',0,'C',1)
                pdf.multi_cell(85,5,str(u['nombre']).decode("UTF-8"),'LTR','J',1)
                pdf.set_y(38+c)
                pdf.set_x(223)
                pdf.cell(20,10,str(u['telefono']),'LTBR',0,'C',1)
                pdf.cell(20,10,str(u['tot_ins']),'LTBR',1,'C',1)
                pdf.cell(250,0.1,'','T',1,'C',1)

                pdf.set_fill_color(255,255,255)
                pdf.set_font('Arial','B',8)
                
                pdf.set_fill_color(255,255,255)
                pdf.set_font('Arial','B',8)

                c = c + 10
                a = a + 1
                total += tot_ins
                tamano = 128
                tamano1 = 105
         
        pdf.set_font('Arial','B',13)
        pdf.cell(tamano,10,'','R',0,'C',1)
        pdf.cell(tamano1,10,'Total de 1X10','LTBR',0,'C',1)
        pdf.set_font('Arial','B',13)
        pdf.cell(20,10,str(total),'LTBR',1,'C',1)

        ruta_reporte = settings.MEDIA_PDF
        archivo = ruta_reporte + '/' + 'listado1x10ubch.pdf'
        pdf.output(archivo, 'F')
        archivo = open(archivo, "r")
        response = HttpResponse(archivo.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="' + str(archivo) + '.pdf"'

        return response

            # ============================================================================


def dictfetchall(cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
