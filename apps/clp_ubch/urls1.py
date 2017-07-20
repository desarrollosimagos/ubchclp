from django.conf.urls import patterns, url
from .views import RegistroClpUbch, UbchView, ClpUbchView, ClpUbchReport, ReporteClpUbch

urlpatterns = patterns('',
                       url(r'^registro/$', RegistroClpUbch.as_view(), name='registro_clpubch'),
                       url(r'^lista/cod_ubch=(?P<cod_ubch>\d+)$',
                           UbchView.as_view()
                           ),
                       url(r'^cod_clp=(?P<cod_clp>\d+)/$',
                           ClpUbchView.as_view()
                           ),
                       #url(r'^cedula_jefe=(?P<cedula_jefe>\d+)$',
                       #    ClpUbchListView.as_view()
                       #    ),
                       #url(r'^reporte/(?P<filename>[a-z0-9A-Z_\-]*\.pdf)$', ClpUbchReport.as_view()),
                       url(r'^reporte/(?P<cod_circulo>\d+)$', ClpUbchReport.as_view()),
                       url(r'^clpubch/$', ReporteClpUbch.as_view(), name='clpubch'),
                       )
