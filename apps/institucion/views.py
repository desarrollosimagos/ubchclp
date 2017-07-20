from .models import Intitucion
from django.views.generic import CreateView

class RegistrarUnoPorDiez(CreateView):
    template_name = 'registro/institucion.html'
    model = UnoPorDiez

    def post(self, request, *args, **kwargs):
        print self.request.POST
