from django.conf.urls import patterns, url
from views import RegistrarUnoPorDiez, UnoPorDiezView, Reporte1x10, Lista1x10Report, Listar1X10,Lista1x10ubchReport, RegistrarUnoPorJefeInst
urlpatterns = patterns('',
                       url(r'^registro/$', RegistrarUnoPorDiez.as_view(),
                           name="registro_uno"),
                       url(r'^lista/cedula_patrullero=(?P<cedula_patrullero>\d+)$',
                           UnoPorDiezView.as_view()
                           ),
                       url(r'^unoordiez/$', Reporte1x10.as_view(),
                           name='reporte_unodiez'),
                       url(r'^reporte/(?P<cedula>\d+)$', Lista1x10Report.as_view()),
                       url(r'^listar/(?P<cedula>\d+)$', Listar1X10.as_view()),
                       url(r'^reporte/(?P<tipo>\w+)$', Lista1x10ubchReport.as_view()), # Url para la consulta de listado de 1x10 por ubch
                       url(r'^registro_unojefes/$', RegistrarUnoPorJefeInst.as_view(),
                           name="registro_unojefes"),
                       )
                         
