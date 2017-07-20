#encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from .models import Estado
from .forms import FormEstado
from django.views.generic.dates import ArchiveIndexView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response
from django.contrib import messages # Metodo para la validacion de los campos
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Paginacion
from django.contrib.auth.decorators import login_required # Forma para impedir el acceso al sistema
import os
import csv
#=====================================================================================
#                            # Clase RegistrarEstado
#=====================================================================================
@login_required(login_url='/')
def RegistrarEstado(request):
    if request.method=='POST':
        form_regestado = FormEstado(request.POST, request.FILES)
        if form_regestado.is_valid():
            nuevo_regestado = form_regestado.save(commit=False)
            nuevo_regestado.user = request.user.username
            nuevo_regestado.save()
	    return HttpResponseRedirect('/estado/lista_estado')
    else:
         form_regestado = FormEstado()
    ctx = {'form_regestado':form_regestado} # ctx = Contexto
    return render_to_response('topologia/estado/registrar_estado.html',ctx, context_instance=RequestContext(request))
    

#=====================================================================================
                            # Clase ActualizarEstado
#=====================================================================================
@login_required(login_url='/')
def ActualizarEstado(request,pk):
    obj_regestado = Estado.objects.get(id=pk)
    if request.method=='POST':
        form_regestado = FormEstado(request.POST, request.FILES, instance=obj_regestado)
        if form_regestado.is_valid():
            edit_regestado = form_regestado.save(commit=False)
            edit_regestado.user = request.user.username
            edit_regestado.save()
            return HttpResponseRedirect('/estado/lista_estado')
    else:
        form_regestado = FormEstado(instance=obj_regestado)
    ctx = {'form_regestado':form_regestado,'obj_regestado':obj_regestado} # ctx = Contexto
    return render_to_response('topologia/estado/actualizar_estado.html',ctx, context_instance=RequestContext(request))

#=====================================================================================
                            # Clase EliminarEstado
#=====================================================================================
def EliminarEstado(request,pk):
    obj_regestado = Estado.objects.get(id=pk)
    obj_regestado.delete()
    return HttpResponseRedirect('/estado/lista_estado')
#======================================================================================
# Metodo para listar Registros y Paginacion
#======================================================================================
@login_required(login_url='/')
def ListarEstado(request):
    estado    = Estado.objects.all()
    paginator = Paginator(estado, 5) # Show 5 contacts per page
    page      = request.GET.get('page')
    try:
        lista_estados    = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        lista_estados = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        lista_estados = paginator.page(paginator.num_pages)
    ctx          = {'lista_estados':lista_estados,} # ctx = Contexto
    return render_to_response('topologia/estado/lista_estado.html',ctx, context_instance=RequestContext(request))

#======================================================================================
                    # Metodo para renderizar a /
#=====================================================================================

def base_view(request):
    
    return render_to_response('base/base.html',locals(), context_instance=RequestContext(request))
#======================================================================================
# Url Importar data CSV
#======================================================================================
@login_required(login_url='/')
def load_data(request):

    os.path.dirname(os.path.abspath(__file__))

    DIR_URL = os.getcwd()

    reader = csv.reader(open(DIR_URL+str("/apps/topologia/estados/script/estados.csv")))
    
    # Recorrido de los registros
    for row in reader:
        data = row[0].split(';')
        centro = Estado(
            cod_estado     = data[0],
            estado         = data[1],
            )
        centro.save()
    return HttpResponseRedirect('/estado/lista_estado')
#======================================================================================

def custom_404(request):
    return render_to_response('404.html', RequestContext(request))
