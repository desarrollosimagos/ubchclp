# -*- coding: utf-8 -*-

import datetime
from django.contrib.auth.models import User
from django.db import connection
from django.db.models.aggregates import Count
from django.http import HttpResponse

from django.views.generic import ListView, CreateView, DetailView, UpdateView
import sys
from apps.registro_ubch import class_report
from apps.unodiezinti.models import UnoDiezInti
from .models import Datos
from passlib.hash import django_pbkdf2_sha256 as handler
import json
from django.contrib.auth import  logout
from ubch import settings


class ListDatosView(ListView):
    template_name = 'datos/listar.html'
    model = Datos

    def get_context_data(self, **kwargs):
        context = super(ListDatosView, self).get_context_data(**kwargs)

        current_user = self.request.user.id
        datos = Datos.objects.all()
        unodiez = UnoDiezInti.objects.all()

        unodiez_f = unodiez.filter(usuario_id=current_user)
        unodiez_v = unodiez_f.values('datos_id')

        datos_f = datos.exclude(usuario_id=current_user).exclude(id__in=unodiez_v)
        datos_v = datos_f.values('id', 'cedula', 'p_nombre', 's_nombre', 'p_apellido', 's_apellido', 'telefono', 'departamento')

        context['listado'] = datos_v
        return context


class DetailDatosView(DetailView):
    model = Datos
    template_name = 'datos/detail.html'

    def get(self, request, *args, **kwargs):

        current_user = self.request.user
        user_cedula = current_user.datos.cedula

        response_data = {}
        cedula = self.request.GET.get('cedula')

        if int(cedula) == int(user_cedula):
            response_data['misma'] = 'ok'
            return HttpResponse(json.dumps(response_data), status=200, content_type='application/json')
        else:

            datos = Datos.objects.all()

            datos_f = datos.filter(cedula=cedula)
            datos_v = datos_f.values('id', 'p_nombre', 's_nombre', 'p_apellido', 's_apellido',)

            data = {}
            for d in datos_v:
                data = d

            unodiez = UnoDiezInti.objects.all()

            unodiez_f = unodiez.filter(datos_id=data['id'], usuario_id=current_user.id)

            if unodiez_f.exists():
                response_data['existe'] = 'ok'
                return HttpResponse(json.dumps(response_data), status=200, content_type='application/json')
            else:
                response_data['datos'] = data
                return HttpResponse(json.dumps(response_data), status=200, content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(DetailDatosView, self).get_context_data(**kwargs)

        datos_id = self.kwargs['pk']

        datos = Datos.objects.all()

        datos_f = datos.filter(id=datos_id)
        datos_v = datos_f.values('id','cedula', 'p_nombre', 's_nombre', 'p_apellido', 's_apellido', 'telefono', 'departamento')

        data = {}
        for d in datos_v:
            data = d
        context['detail'] = data
        return context


class RegistroView(CreateView):
    model = UnoDiezInti
    template_name = 'datos/registro.html'

    def post(self, request, *args, **kwargs):
        id_emp = self.request.POST.get('id_emp')
        current_user = self.request.user.id

        grupo_usuario = self.request.user.datos.grupo_usuario

        datos = UnoDiezInti.objects.all()
        datos_f = datos.filter(usuario_id=current_user)

        count_datos = datos_f.count()

        response_data = {}
        if count_datos < 10:

            datos_n = Datos.objects.all()
            datos_n_f = datos_n.filter(id=id_emp)
            usuario_id  = datos_n_f.values('usuario_id')

            datos_user = User.objects.all()
            datos_user_f = datos_user.filter(id=usuario_id)
            datos_user_f.update(is_active=True)

            add = UnoDiezInti()
            add.datos_id = id_emp
            add.usuario_id =current_user
            add.save()
            count_datos = datos_f.count()
            if count_datos == 10:

                datos_user_f = datos_user.filter(id=current_user)

                if grupo_usuario == 3:
                    datos_user_f.update(is_active=False)
                    logout(request)
                    response_data['admin'] = 'no'
                else:
                    response_data['admin'] = 'si'

                response_data['culminado'] = 'ok'
                return HttpResponse(json.dumps(response_data), status=200, content_type='application/json')
            else:
                response_data['success'] = 'ok'
                return HttpResponse(json.dumps(response_data), status=200, content_type='application/json')
        else:
            response_data['diez'] = 'ok'
            return HttpResponse(json.dumps(response_data), status=200, content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(RegistroView, self).get_context_data(**kwargs)

        current_user = self.request.user.id

        datos = UnoDiezInti.objects.all()
        datos_f = datos.filter(usuario_id=current_user)

        print datos_f.count()

        datos_v =  datos_f.values('datos__cedula', 'datos__p_nombre', 'datos__s_nombre', 'datos__p_apellido', 'datos__s_apellido', 'datos__telefono', 'datos__departamento')
        context['listado'] = datos_v
        return context


class LoginView(CreateView):
    model = UnoDiezInti
    template_name = 'datos/registro.html'

    def post(self, request, *args, **kwargs):
        current_user = self.request.user.id
        string_date = self.request.POST.get('fecha')
        fecha = datetime.datetime.strptime(string_date, "%d/%m/%Y")
        datos = Datos.objects.all()
        datos_f = datos.filter(fecha_naci=fecha, usuario_id=current_user)

        response_data = {}
        if datos_f.exists():
            response_data['success'] = 'ok'
            return HttpResponse(json.dumps(response_data), status=200, content_type='application/json')
        else:
            response_data['error'] = 'ok'
            return HttpResponse(json.dumps(response_data), status=200, content_type='application/json')


class MiListaView(ListView):
    template_name = 'datos/milista.html'
    model = UnoDiezInti

    def get_context_data(self, **kwargs):
        context = super(MiListaView, self).get_context_data(**kwargs)

        current_user = self.request.user.id

        datos = UnoDiezInti.objects.all()
        datos_f = datos.filter(usuario_id=current_user)


        datos_v =  datos_f.values('datos__cedula', 'datos__p_nombre', 'datos__s_nombre', 'datos__p_apellido', 'datos__s_apellido', 'datos__telefono', 'datos__departamento')
        context['listado'] = datos_v
        return context


class ListPatrullerosView(ListView):
    template_name = 'datos/patrulleros.html'
    model = Datos

    def get_context_data(self, **kwargs):
        context = super(ListPatrullerosView, self).get_context_data(**kwargs)

        usuario = UnoDiezInti.objects.all()

        usuario_id = usuario.values('usuario_id').distinct()

        datos = Datos.objects.all()

        datos_v = datos.values('usuario_id','cedula','p_nombre','s_nombre', 'p_apellido', 's_apellido', 'telefono','cargo' ,'departamento').order_by('cedula')
        #datos_f = datos_v.filter(usuario_id__in=usuario_id)
	datos_f = datos_v.filter(id__in=usuario_id)

        usuario_f = usuario.values('datos__usuario_id','datos__cedula', 'datos__p_nombre').filter(datos__usuario_id__in=usuario_id).annotate(total=Count('datos__usuario_id')).distinct()
        print usuario_f

        context['listado'] = datos_f
        return context



class ListNoCargaView(ListView):
    template_name = 'datos/nocarga.html'
    model = Datos

    def get_context_data(self, **kwargs):
        context = super(ListNoCargaView, self).get_context_data(**kwargs)

        usuario = UnoDiezInti.objects.all()

        usuario_id = usuario.values('usuario_id').distinct()

        datos = Datos.objects.all()

        datos_id = usuario.values('datos_id').distinct()
        #datos_f = datos.filter(usuario_id__in=datos_id).exclude(usuario_id__in=usuario_id)
	datos_f = datos.filter(id__in=datos_id).exclude(id__in=usuario_id)
        datos_v = datos_f.values('usuario_id','cedula','p_nombre','s_nombre', 'p_apellido', 's_apellido', 'telefono','cargo' ,'departamento').order_by('cedula')

        context['listado'] = datos_v
        return context


class ListJefesView(ListView):
    template_name = 'datos/jefes.html'
    model = Datos

    def get_context_data(self, **kwargs):
        context = super(ListJefesView, self).get_context_data(**kwargs)

        datos = UnoDiezInti.objects.all()
        usuario_id = datos.values('usuario_id').distinct()
        datos_i = datos.filter(datos__usuario_id__in=usuario_id)
        datos_v = datos_i.values('datos__usuario_id','datos__cedula','datos__p_nombre','datos__s_nombre', 'datos__p_apellido', 'datos__s_apellido', 'datos__cargo' ,'datos__departamento').filter(datos__grupo_usuario__lt=3).distinct().order_by('datos__cedula')

        context['listado'] = datos_v
        return context


class ReporteDatosView(DetailView):
    model = Datos
    template_name = 'datos/detail.html'

    def get(self, request, *args, **kwargs):

        reload(sys)

        sys.setdefaultencoding("utf-8")
        pdf = class_report.PDFBV(orientation='P',  unit='mm', format='letter' )


        pdf.set_author('Marcel Arcuri')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_fill_color(157, 188, 201)
        pdf.set_text_color(24, 29, 31)
        pdf.set_margins(10, 10, 10)

        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(27, 128, 172)
        # pdf.cell(250, 5, 'Patriotas BVA 200', '', 1, 'C', 0)
        pdf.ln()

        pdf.set_x(40)
        pdf.set_text_color(0, 0, 0)
        pdf.set_fill_color(217, 237, 247)
        pdf.set_font('Arial', 'B', 8)  # Fuente de la Letra
        pdf.cell(10, 5, 'Nº'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
        pdf.cell(18, 5, 'Cédula'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
        pdf.cell(80, 5, 'Nombre'.decode("UTF-8"), 'LTRB', 0, 'L', 1)
        pdf.cell(22, 5, 'Cant Patrullas', 'LTRB', 1, 'L', 1)
        datos = UnoDiezInti.objects.all()
        datos_v = datos.values("datos_id",'datos__cedula','datos__p_nombre','datos__s_nombre', 'datos__p_apellido', 'datos__s_apellido').annotate(total = Count("datos_id")).order_by('-total')

        i = 1
        j = 1
        for d in datos_v:

            if j == 45:
                pdf.add_page()
                pdf.set_x(40)
                pdf.set_text_color(0, 0, 0)
                pdf.set_fill_color(217, 237, 247)
                pdf.set_font('Arial', 'B', 8)  # Fuente de la Letra
                pdf.cell(10, 5, 'Nº'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
                pdf.cell(18, 5, 'Cédula'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
                pdf.cell(80, 5, 'Nombre'.decode("UTF-8"), 'LTRB', 0, 'L', 1)
                pdf.cell(22, 5, 'Cant Patrullas', 'LTRB', 1, 'L', 1)
                j=1

            resto = i % 2
            s_nombre = ''
            if d['datos__s_nombre'] is not None:
               s_nombre  =   d['datos__s_nombre']

            s_apellido = ''
            if d['datos__s_apellido'] is not None:
               s_apellido  =   d['datos__s_apellido']

            pdf.set_x(40)
            pdf.set_fill_color(255, 255, 255)

            if resto == 0:
                pdf.set_fill_color(239, 239, 239)

            pdf.set_font('Arial', '', 8)  # Fuente de la Letra
            pdf.cell(10, 5, str(i), 'LTRB', 0, 'R', 1)
            pdf.cell(18, 5, str(d['datos__cedula']), 'LTRB', 0, 'R', 1)
            pdf.cell(80, 5, str(d['datos__p_nombre']).decode("UTF-8")+' '+str(s_nombre).decode("UTF-8")+' '+str(d['datos__p_apellido']).decode("UTF-8")+' '+str(s_apellido).decode("UTF-8"), 'LTRB', 0, 'L', 1)
            pdf.cell(22, 5, str(d['total']), 'LTRB', 1, 'R', 1)
            i += 1
            j += 1
        arch = 'patrullero'
        ruta_reporte = settings.MEDIA_PDF
        archivo = ruta_reporte+'patriotas.pdf'
        pdf.output(archivo, 'F')
        archivo = open(archivo, "r")
        response = HttpResponse(archivo.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="'+str(arch)+'.pdf"'
        return response


class ReportePatrullerosView(DetailView):
    model = Datos
    template_name = 'datos/detail.html'

    def get(self, request, *args, **kwargs):

        reload(sys)

        sys.setdefaultencoding("utf-8")
        pdf = class_report.PDFBV(orientation='P',  unit='mm', format='letter' )

        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_fill_color(157, 188, 201)
        pdf.set_text_color(24, 29, 31)
        pdf.set_margins(10, 10, 10)

        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(27, 128, 172)
        # pdf.cell(250, 5, 'Patriotas BVA 200', '', 1, 'C', 0)

        m_x = 20

        pdf.set_x(m_x)
        pdf.set_text_color(0, 0, 0)
        pdf.set_fill_color(217, 237, 247)
        pdf.set_font('Arial', 'B', 11)  # Fuente de la Letra
        pdf.cell(180, 5, 'Listado con 1x10'.decode("UTF-8"), 0, 1, 'C', 0)

        pdf.set_x(m_x)
        pdf.set_font('Arial', 'B', 8)  # Fuente de la Letra
        pdf.cell(10, 5, 'Nº'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
        pdf.cell(18, 5, 'Cédula'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
        pdf.cell(70, 5, 'Nombre'.decode("UTF-8"), 'LTRB', 0, 'L', 1)
        pdf.cell(80, 5, 'Cargo', 'LTRB', 1, 'L', 1)

        usuario = UnoDiezInti.objects.all()
        usuario_id = usuario.values('usuario_id').distinct()
        datos = Datos.objects.all()
        datos_f = datos.filter(usuario_id__in=usuario_id)
        datos_v = datos_f.values('usuario_id','cedula','p_nombre','s_nombre', 'p_apellido', 's_apellido', 'telefono','cargo' ,'departamento').order_by('cedula')

        i = 1
        j = 1
        for d in datos_v:

            if j == 45:
                pdf.add_page()
                pdf.set_x(m_x)
                pdf.set_text_color(0, 0, 0)
                pdf.set_fill_color(217, 237, 247)
                pdf.set_font('Arial', 'B', 8)  # Fuente de la Letra
                pdf.cell(10, 5, 'Nº'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
                pdf.cell(18, 5, 'Cédula'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
                pdf.cell(70, 5, 'Nombre'.decode("UTF-8"), 'LTRB', 0, 'L', 1)
                pdf.cell(80, 5, 'Cargo', 'LTRB', 1, 'L', 1)
                j=1

            resto = i % 2
            s_nombre = ''
            if d['s_nombre'] is not None:
               s_nombre  =   d['s_nombre']

            s_apellido = ''
            if d['s_apellido'] is not None:
               s_apellido  =   d['s_apellido']

            cargo = ''
            if d['cargo'] is not None:
               cargo  =   d['cargo']

            pdf.set_x(m_x)
            pdf.set_fill_color(255, 255, 255)

            if resto == 0:
                pdf.set_fill_color(239, 239, 239)

            pdf.set_font('Arial', '', 8)  # Fuente de la Letra
            pdf.cell(10, 5, str(i), 'LTRB', 0, 'R', 1)
            pdf.cell(18, 5, str(d['cedula']), 'LTRB', 0, 'R', 1)
            pdf.cell(70, 5, str(d['p_nombre']).decode("UTF-8")+' '+str(s_nombre).decode("UTF-8")+' '+str(d['p_apellido']).decode("UTF-8")+' '+str(s_apellido).decode("UTF-8"), 'LTRB', 0, 'L', 1)
            pdf.cell(80, 5, str(cargo), 'LTRB', 1, 'L', 1)

            i += 1
            j += 1
        arch = 'patrullero'
        ruta_reporte = settings.MEDIA_PDF
        archivo = ruta_reporte+'patriotas.pdf'
        pdf.output(archivo, 'F')
        archivo = open(archivo, "r")
        response = HttpResponse(archivo.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="'+str(arch)+'.pdf"'
        return response


class ReporteNoCargaView(DetailView):
    model = Datos
    template_name = 'datos/detail.html'

    def get(self, request, *args, **kwargs):

        reload(sys)

        sys.setdefaultencoding("utf-8")
        pdf = class_report.PDFBV(orientation='P',  unit='mm', format='letter' )

        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_fill_color(157, 188, 201)
        pdf.set_text_color(24, 29, 31)
        pdf.set_margins(10, 10, 10)

        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(27, 128, 172)
        # pdf.cell(250, 5, 'Patriotas BVA 200', '', 1, 'C', 0)

        m_x = 20

        pdf.set_x(m_x)
        pdf.set_text_color(0, 0, 0)
        pdf.set_fill_color(217, 237, 247)
        pdf.set_font('Arial', 'B', 11)  # Fuente de la Letra
        pdf.cell(180, 5, 'Listado sin 1x10'.decode("UTF-8"), 0, 1, 'C', 0)
        pdf.set_font('Arial', 'B', 8)  # Fuente de la Letra

        pdf.set_x(m_x)
        pdf.cell(10, 5, 'Nº'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
        pdf.cell(18, 5, 'Cédula'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
        pdf.cell(70, 5, 'Nombre'.decode("UTF-8"), 'LTRB', 0, 'L', 1)
        pdf.cell(80, 5, 'Cargo', 'LTRB', 1, 'L', 1)

        usuario = UnoDiezInti.objects.all()
        usuario_id = usuario.values('usuario_id').distinct()
        datos = Datos.objects.all()
        datos_id = usuario.values('datos_id').distinct()
        datos_f = datos.filter(usuario_id__in=datos_id).exclude(usuario_id__in=usuario_id)
        datos_v = datos_f.values('usuario_id','cedula','p_nombre','s_nombre', 'p_apellido', 's_apellido', 'telefono','cargo' ,'departamento').order_by('cedula')

        i = 1
        j = 1
        for d in datos_v:

            if j == 45:
                pdf.add_page()
                pdf.set_x(m_x)
                pdf.set_text_color(0, 0, 0)
                pdf.set_fill_color(217, 237, 247)
                pdf.set_font('Arial', 'B', 8)  # Fuente de la Letra
                pdf.cell(10, 5, 'Nº'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
                pdf.cell(18, 5, 'Cédula'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
                pdf.cell(70, 5, 'Nombre'.decode("UTF-8"), 'LTRB', 0, 'L', 1)
                pdf.cell(80, 5, 'Cargo', 'LTRB', 1, 'L', 1)
                j=1

            resto = i % 2
            s_nombre = ''
            if d['s_nombre'] is not None:
               s_nombre  =   d['s_nombre']

            s_apellido = ''
            if d['s_apellido'] is not None:
               s_apellido = d['s_apellido']

            pdf.set_x(m_x)
            pdf.set_fill_color(255, 255, 255)

            if resto == 0:
                pdf.set_fill_color(239, 239, 239)

            pdf.set_font('Arial', '', 8)  # Fuente de la Letra
            pdf.cell(10, 5, str(i), 'LTRB', 0, 'R', 1)
            pdf.cell(18, 5, str(d['cedula']), 'LTRB', 0, 'R', 1)
            pdf.cell(70, 5, str(d['p_nombre']).decode("UTF-8")+' '+str(s_nombre).decode("UTF-8")+' '+str(d['p_apellido']).decode("UTF-8")+' '+str(s_apellido).decode("UTF-8"), 'LTRB', 0, 'L', 1)
            pdf.cell(80, 5, str(d['cargo']), 'LTRB', 1, 'L', 1)

            i += 1
            j += 1
        arch = 'patrullero'
        ruta_reporte = settings.MEDIA_PDF
        archivo = ruta_reporte+'patriotas.pdf'
        pdf.output(archivo, 'F')
        archivo = open(archivo, "r")
        response = HttpResponse(archivo.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="'+str(arch)+'.pdf"'
        return response


class ReportePatrullerosJefesView(DetailView):
    model = Datos
    template_name = 'datos/detail.html'

    def get(self, request, *args, **kwargs):

        reload(sys)

        sys.setdefaultencoding("utf-8")
        pdf = class_report.PDFBV(orientation='P',  unit='mm', format='letter' )

        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_fill_color(157, 188, 201)
        pdf.set_text_color(24, 29, 31)
        pdf.set_margins(10, 10, 10)

        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(27, 128, 172)
        # pdf.cell(250, 5, 'Patriotas BVA 200', '', 1, 'C', 0)
        pdf.ln()

        pdf.set_x(10)
        pdf.set_text_color(0, 0, 0)
        pdf.set_fill_color(217, 237, 247)
        pdf.set_font('Arial', 'B', 8)  # Fuente de la Letra
        pdf.cell(10, 5, 'Nº'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
        pdf.cell(18, 5, 'Cédula'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
        pdf.cell(70, 5, 'Nombre'.decode("UTF-8"), 'LTRB', 0, 'L', 1)
        pdf.cell(80, 5, 'Cargo', 'LTRB', 1, 'L', 1)


        datos = UnoDiezInti.objects.all()
        usuario_id = datos.values('usuario_id').distinct()
        datos_i = datos.filter(datos__usuario_id__in=usuario_id)
        datos_v = datos_i.values("datos_id",'datos__cedula','datos__p_nombre','datos__s_nombre', 'datos__p_apellido', 'datos__s_apellido', 'datos__cargo' ,'datos__departamento').filter(datos__grupo_usuario__lt=3).distinct().order_by('datos__cedula')

        i = 1
        j = 1
        for d in datos_v:

            if j == 45:
                pdf.add_page()
                pdf.set_x(10)
                pdf.set_text_color(0, 0, 0)
                pdf.set_fill_color(217, 237, 247)
                pdf.set_font('Arial', 'B', 8)  # Fuente de la Letra
                pdf.cell(10, 5, 'Nº'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
                pdf.cell(18, 5, 'Cédula'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
                pdf.cell(70, 5, 'Nombre'.decode("UTF-8"), 'LTRB', 0, 'L', 1)
                pdf.cell(80, 5, 'Cargo', 'LTRB', 1, 'L', 1)
                j=1

            resto = i % 2
            s_nombre = ''
            if d['datos__s_nombre'] is not None:
               s_nombre  =   d['datos__s_nombre']

            s_apellido = ''
            if d['datos__s_apellido'] is not None:
               s_apellido  =   d['datos__s_apellido']

            pdf.set_x(10)
            pdf.set_fill_color(255, 255, 255)

            if resto == 0:
                pdf.set_fill_color(239, 239, 239)

            pdf.set_font('Arial', '', 8)  # Fuente de la Letra
            pdf.cell(10, 5, str(i), 'LTRB', 0, 'R', 1)
            pdf.cell(18, 5, str(d['datos__cedula']), 'LTRB', 0, 'R', 1)
            pdf.cell(70, 5, str(d['datos__p_nombre']).decode("UTF-8")+' '+str(s_nombre).decode("UTF-8")+' '+str(d['datos__p_apellido']).decode("UTF-8")+' '+str(s_apellido).decode("UTF-8"), 'LTRB', 0, 'L', 1)
            pdf.cell(80, 5, str(d['datos__cargo']), 'LTRB', 1, 'L', 1)

            i += 1
            j += 1
        arch = 'patrullero'
        ruta_reporte = settings.MEDIA_PDF
        archivo = ruta_reporte+'patriotas.pdf'
        pdf.output(archivo, 'F')
        archivo = open(archivo, "r")
        response = HttpResponse(archivo.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="'+str(arch)+'.pdf"'
        return response


class ReportePatrullerosDetailView(DetailView):
    model = Datos
    template_name = 'datos/detail.html'

    def get(self, request, *args, **kwargs):

        reload(sys)
        datos_id = self.kwargs['pk']
        sys.setdefaultencoding("utf-8")
        pdf = class_report.PDFBV(orientation='P',  unit='mm', format='letter' )

        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_fill_color(157, 188, 201)
        pdf.set_text_color(24, 29, 31)
        pdf.set_margins(10, 10, 10)

        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(27, 128, 172)
        # pdf.cell(250, 5, 'Patriotas BVA 200', '', 1, 'C', 0)

        patrullero = Datos.objects.all()
        patrullero_f = patrullero.filter(usuario_id=datos_id)
        patrullero_v = patrullero_f.values('cedula', 'p_nombre', 's_nombre', 'p_apellido', 's_apellido', 'cargo')

        cedula = '{:,}'.format(patrullero_v[0]['cedula']).replace(",", ".")

        print cedula


        m_x = 20

        pdf.set_x(m_x)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', 'B', 11)  # Fuente de la Letra
        pdf.cell(15, 5, 'Cedula:', 0, 0, 'L', 0)
        pdf.set_font('Arial', '', 11)  # Fuente de la Letra
        pdf.cell(22, 5, str(patrullero_v[0]['cedula']), 0, 0, 'L', 0)



        s_nombre_p = ''
        if patrullero_v[0]['s_nombre'] is not None:
              s_nombre_p  =   patrullero_v[0]['s_nombre']

        s_apellido_p = ''
        if patrullero_v[0]['s_apellido'] is not None:
               s_apellido_p  = patrullero_v[0]['s_apellido']


        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Arial', 'B', 11)  # Fuente de la Letra
        pdf.cell(17, 5, 'Nombre:', 0, 0, 'L', 0)
        pdf.set_font('Arial', '', 11)  # Fuente de la Letra
        pdf.cell(10, 5, str(patrullero_v[0]['p_nombre']+' '+s_nombre_p+' '+patrullero_v[0]['p_apellido']+' '+s_apellido_p).decode("UTF-8"), 0, 0, 'L', 0)

        pdf.ln(15)
        pdf.set_font('Arial', 'B', 11)  # Fuente de la Letra
        pdf.cell(180, 5, 'Lista 1X10', 0, 0, 'C', 0)
        pdf.ln()

        pdf.set_x(m_x)
        pdf.set_text_color(0, 0, 0)
        pdf.set_fill_color(217, 237, 247)
        pdf.set_font('Arial', 'B', 8)  # Fuente de la Letra
        pdf.cell(10, 5, 'Nº'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
        pdf.cell(18, 5, 'Cédula'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
        pdf.cell(70, 5, 'Nombre'.decode("UTF-8"), 'LTRB', 0, 'L', 1)
        pdf.cell(80, 5, 'Cargo', 'LTRB', 1, 'L', 1)

        datos = UnoDiezInti.objects.all()
        datos_i = datos.filter(usuario_id=datos_id)
        datos_v = datos_i.values("datos_id",'datos__cedula','datos__p_nombre','datos__s_nombre', 'datos__p_apellido', 'datos__s_apellido', 'datos__cargo' ,'datos__departamento').distinct().order_by('datos__cedula')

        i = 1
        j = 1
        for d in datos_v:

            if j == 45:
                pdf.add_page()
                pdf.set_x(m_x)
                pdf.set_text_color(0, 0, 0)
                pdf.set_fill_color(217, 237, 247)
                pdf.set_font('Arial', 'B', 8)  # Fuente de la Letra
                pdf.cell(10, 5, 'Nº'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
                pdf.cell(18, 5, 'Cédula'.decode("UTF-8"), 'LTRB', 0, 'C', 1)
                pdf.cell(70, 5, 'Nombre'.decode("UTF-8"), 'LTRB', 0, 'L', 1)
                pdf.cell(80, 5, 'Cargo', 'LTRB', 1, 'L', 1)
                j=1

            resto = i % 2
            s_nombre = ''
            if d['datos__s_nombre'] is not None:
              s_nombre  =   d['datos__s_nombre']

            s_apellido = ''
            if d['datos__s_apellido'] is not None:
               s_apellido  =   d['datos__s_apellido']

            pdf.set_x(m_x)
            pdf.set_fill_color(255, 255, 255)

            if resto == 0:
                pdf.set_fill_color(239, 239, 239)

            pdf.set_font('Arial', '', 8)  # Fuente de la Letra
            pdf.cell(10, 5, str(i), 'LTRB', 0, 'R', 1)
            pdf.cell(18, 5, str(d['datos__cedula']), 'LTRB', 0, 'R', 1)
            pdf.cell(70, 5, str(d['datos__p_nombre']).decode("UTF-8")+' '+str(s_nombre).decode("UTF-8")+' '+str(d['datos__p_apellido']).decode("UTF-8")+' '+str(s_apellido).decode("UTF-8"), 'LTRB', 0, 'L', 1)
            pdf.cell(80, 5, str(d['datos__cargo']), 'LTRB', 1, 'L', 1)

            i += 1
            j += 1
        arch = 'patrullero'
        ruta_reporte = settings.MEDIA_PDF
        archivo = ruta_reporte+'patriotas.pdf'
        pdf.output(archivo, 'F')
        archivo = open(archivo, "r")
        response = HttpResponse(archivo.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="'+str(arch)+'.pdf"'
        return response


class UpdateDatosView(CreateView):
    template_name = 'datos/update.html'
    model = Datos

    def get(self, request, *args, **kwargs):

        cursor = connection.cursor()
        sql = "SELECT ced_num, apellido1, apellido2, nombre1, nombre2, cargo, fecha_naci, direccion, telefono, estatus, fecha_ingreso, tipo_empledo, departamento FROM datos_personales;"

        cursor.execute(sql)
        rows = dictfetchall(cursor)
        for row in rows:

            usuario_name = row['ced_num']
            usuario_clave = row['nombre1'][:1]
            usuario_clave = usuario_clave+row['apellido1']
            usuario_clave = usuario_clave.lower()
            clave = handler.encrypt(usuario_clave)

            useradd = User()

            useradd.username = usuario_name
            useradd.password = clave
            useradd.first_name = row['nombre1']
            useradd.last_name = row['apellido1']
            # useradd.save()

            ultimo = useradd.id
            add = Datos()
            add.cedula = row['ced_num']
            add.p_nombre = row['nombre1']
            add.s_nombre = row['nombre2']
            add.p_apellido = row['apellido1']
            add.s_apellido = row['apellido2']
            add.cargo = row['cargo']
            add.fecha_naci = datetime.datetime.strptime(row['fecha_naci'], '%d/%m/%Y').strftime('%Y-%m-%d')
            add.telefono = row['telefono']
            add.estatus = row['estatus']
            add.fecha_ingreso = datetime.datetime.strptime(row['fecha_ingreso'], '%d/%m/%Y').strftime('%Y-%m-%d')
            add.tipo_empledo = row['tipo_empledo']
            add.departamento = row['departamento']
            add.direccion = row['direccion']
            add.grupo_usuario = 3
            add.usuario_id = ultimo
            # add.save()

        return HttpResponse('<div>>Actualizando...</div>')


class UpdateDatosPassView(UpdateView):
    template_name = 'datos/update.html'
    model = Datos

    def get(self, request, *args, **kwargs):

        id_user= self.kwargs['pk']

        datos_n = Datos.objects.get(usuario_id=id_user)
        nombre = datos_n.p_nombre.strip()[:1]
        apellido = datos_n.p_apellido
        usuario_clave = nombre+apellido

        usuario_clave = usuario_clave.lower()
        clave = handler.encrypt(usuario_clave)

        datos_user = User.objects.all()
        datos_user_f = datos_user.filter(id=id_user)
        datos_user_f.update(password=clave)
        return HttpResponse('<div>Actualizando...</div>')


class CreateDatosUserView(UpdateView):
    template_name = 'datos/update.html'
    model = Datos

    def get(self, request, *args, **kwargs):

        cedula= self.kwargs['cedula']

        datos_n = Datos.objects.get(cedula=cedula)
        nombre = datos_n.p_nombre.strip()
        apellido = datos_n.p_apellido
        usuario_clave = nombre[:1]+apellido

        usuario_clave = usuario_clave.lower()
        clave = handler.encrypt(usuario_clave)

        datos_u = User.objects.all().order_by('-id')[:1]
        datos_u_v = datos_u.values('id')
        ultimo_id_user = datos_u_v[0]['id']+1

        useradd = User()

        useradd.id = ultimo_id_user
        useradd.username = cedula
        useradd.password = clave
        useradd.first_name = nombre
        useradd.last_name = apellido
        useradd.is_active=False
        useradd.save()

        ultimo = useradd.id

        datos_user = Datos.objects.all()
        datos_user_f = datos_user.filter(cedula=cedula)
        datos_user_f.update(usuario_id=ultimo,grupo_usuario=3)

        return HttpResponse('<div>Creando...</div>')


def dictfetchall(cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

