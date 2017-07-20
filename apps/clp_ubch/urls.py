from django.conf.urls import patterns, url
from .views import RegistroClpUbch, UbchView, ClpUbchView, ClpUbchReport, ReporteClpUbch, ListarClpCedula, UbchSearchView, DeleteClpUbchView

urlpatterns = patterns('',
                       url(r'^clp$',ListarClpCedula.as_view(), name="list_registro",),
                       url(r'^registro/$', RegistroClpUbch.as_view(), name='registro_clpubch'),
                       url(r'^lista/cod_ubch=(?P<cod_ubch>\d+)$',
                           UbchView.as_view()
                           ),
                       url(r'^cod_clp=(?P<cod_clp>\d+)/$',
                           ClpUbchView.as_view()
                           ),
                       url(r'^reporte/(?P<cod_circulo>\d+)$', ClpUbchReport.as_view()),
                       url(r'^clpubch/$', ReporteClpUbch.as_view(), name='clpubch'),
                       url(r'^ubch$',UbchSearchView.as_view(), name="list_ubch",),
                       
                       url(r'^eliminar/(?P<pk>\d+)$', DeleteClpUbchView.as_view(), name='eliminar_clpubch'),
                       )
