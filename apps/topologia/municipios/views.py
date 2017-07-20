from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from .models import Municipio # Modelo Municipio
from .forms import FormMunicipio # Vista Forms Municipio
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Paginacion
from django.contrib.auth.decorators import login_required # Forma para impedir el acceso al sistema
import csv # Libreria para inportar CSV
import os
from apps.topologia.estados.models import Estado

#=====================================================================================
#                            # Metodo RegistrarMunicipio
#=====================================================================================
@login_required(login_url='/')
def RegistrarMunicipio(request):
    lista_estado = Estado.objects.all()
    mun          = Municipio.objects.all()
    count_m      = len(mun) + 1
    if request.method=='POST':
        form_reg_mun = FormMunicipio(request.POST, request.FILES)
        if form_reg_mun.is_valid():
            new_reg_mun = form_reg_mun.save(commit=False)
            new_reg_mun.user = request.user.username
            new_reg_mun.save()
	    return HttpResponseRedirect('/municipio/listar_municipios')
    else:
        form_reg_mun = FormMunicipio()
    ctx = {'form_reg_mun':form_reg_mun,'lista_estado':lista_estado,'count_m':count_m }
    return render_to_response('topologia/municipio/registrar_municipio.html',ctx, context_instance=RequestContext(request))

#=====================================================================================
#                            # Clase RegistrarEstado
#=====================================================================================

@login_required(login_url='/')
def ActualizarMunicipio(request,pk):
    lista_estado = Estado.objects.all()
    obj_reg_mun = Municipio.objects.get(id=pk)
    if request.method=='POST':
        form_reg_mun = FormMunicipio(request.POST, request.FILES, instance=obj_reg_mun)
        if form_reg_mun.is_valid():
            edit_reg_mun = form_reg_mun.save(commit=False)
            edit_reg_mun.user = request.user.username
            edit_reg_mun.save()
            return HttpResponseRedirect('/municipio/listar_municipios')
    else:
        form_reg_mun = FormMunicipio(instance=obj_reg_mun)
    ctx = {'form_reg_mun':form_reg_mun,'obj_reg_mun':obj_reg_mun,'lista_estado':lista_estado} # ctx = Contexto
    return render_to_response('topologia/municipio/actualizar_municipio.html',ctx, context_instance=RequestContext(request))

#=====================================================================================
#                            # Clase RegistrarEstado
#=====================================================================================
@login_required(login_url='/')
def EliminarMunicipio(request,pk):
    obj_mun = Municipio.objects.get(id=pk)
    obj_mun.delete()
    return HttpResponseRedirect('/municipio/listar_municipios')

#======================================================================================
              # Metodo para listar Registros y Paginacion
#======================================================================================
@login_required(login_url='/')
def ListarMunicipio(request):
    municipio    = Municipio.objects.all()
    paginator    = Paginator(municipio, 5) # Show 5 contacts per page
    page         = request.GET.get('page')
    try:
        lista_municipio    = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        lista_municipio    = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        lista_municipio    = paginator.page(paginator.num_pages)
    ctx          = {'lista_municipio':lista_municipio,} # ctx = Contexto
    return render_to_response('topologia/municipio/lista_municipio.html',ctx, context_instance=RequestContext(request))

#======================================================================================
# Url Importar data CSV
#======================================================================================
@login_required(login_url='/')
def load_data(request):

    os.path.dirname(os.path.abspath(__file__))

    DIR_URL = os.getcwd()

    reader = csv.reader(open(DIR_URL+str("/apps/topologia/municipios/script/municipio.csv")))
    
    # Recorrido de los registros
    for row in reader:
        data = row[0].split(';')
        centro = Municipio(
            municipio      = data[0],
            cod_municipio  = data[2],
            estado_id      = data[1],
            )
        centro.save()
    return HttpResponseRedirect('/municipio/listar_municipios')
#======================================================================================
