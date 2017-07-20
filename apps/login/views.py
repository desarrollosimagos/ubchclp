# -*- coding: utf-8 -*-
import json
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from apps.unodiezinti.models import UnoDiezInti


class LoginUsuario(TemplateView):
    model = User
    template_name = 'login/login.html'

    def post(self, request, *args, **kwargs):

        username = request.POST.get('username')
        password = request.POST.get('password')

        response_data = {}
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_superuser == False:
                if user.datos.grupo_usuario == 3:
                    if user.is_active:
                        login(request, user)
                        request.session['grupo_id'] = user.datos.grupo_usuario
                        response_data['bva'] = 'ok'

                    else:
                        datos = UnoDiezInti.objects.all()
                        datos_f = datos.filter(usuario_id=user.id)

                        count_datos = datos_f.count()
                        if count_datos == 10:
                            response_data['completa'] = 'ok'
                        else:
                            response_data['active'] = 'no'
                else:
                    login(request, user)
                    request.session['grupo_id'] = user.datos.grupo_usuario
                    response_data['admin'] = 'ok'
            elif user.is_active:
                login(request, user)
                response_data['success'] = 'ok'
        else:
            response_data['error'] = 'ok'

        return HttpResponse(json.dumps(response_data), status=200, content_type='application/json')


def logout_view(request):
    # del request.session['grupo_id']
    logout(request)

    return HttpResponseRedirect('/')
