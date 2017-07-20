# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.login.forms import LoginForm, UserForm
from django.contrib.auth import login, logout, authenticate
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy



def login_view(request):
    """ Vista basada en Metodos o funciones: (`Ingresar`)
    Donde validamos que el usuario y la contraseña del mismo son validos de lo contrario se emite un mensaje.
    """
    mensaje = ""
    if request.user.is_authenticated():
        return HttpResponseRedirect('/menu')
    else:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                usuario = authenticate(username=username, password=password)
                if usuario is not None and usuario.is_active:
                    login(request, usuario)
                    if usuario.is_superuser == False:
                        if usuario.datos.grupo_usuario == 3:
                            #return HttpResponseRedirect('/datos/registro/')
                            return HttpResponseRedirect('/datos/fecha/')
                    else:
                        return HttpResponseRedirect('/menu/')
                else:
                    mensaje = "Usuario y/o Contraseña incorrecto"
        form = LoginForm()
        ctx = {'form': form, 'mensaje': mensaje}
        return render_to_response('login/login.html', ctx, context_instance=RequestContext(request))


class RegistrarUsuario(FormView):
    template_name = 'login/registro_user.html'
    form_class = UserForm
    success_url = reverse_lazy('/')

    def form_valid(self, form):
        user = form.save()
        perfil = PerfilesUsuario()
        perfil.user = user
        perfil.tlf = form.cleaned_data['tlf']
        perfil.user_accion = form.cleaned_data['user_accion']
        perfil.save()
        return super(RegistrarUsuario, self).form_valid(form)


def logout_view(request):
    """ metodo que cierra la sesion y redirecciona al usuario a la pagina de inicio.
    """
    logout(request)
    return HttpResponseRedirect('/')
