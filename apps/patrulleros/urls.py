from django.conf.urls import patterns, url
from .views import RegistrarPatrullero, PatrulleroView, PatrulleroDatosView, ReportePatrullero, PatrulleroReport, DeletePatrullero

urlpatterns = patterns('',
                       url(r'^registro/$', RegistrarPatrullero.as_view(),
                           name='registro_patrullero'),
                       url(r'^cedula_jefe=(?P<cedula_jefe>\d+)$',
                           PatrulleroView.as_view()
                           ),
                       url(r'^$',
                           PatrulleroDatosView.as_view()
                           ),
                       url(r'^patrullero/$', ReportePatrullero.as_view(),
                           name='reporte_patrullero'),
                       url(r'^reporte/(?P<cedula>\d+)$', PatrulleroReport.as_view()),
                       url(r'^eliminar/(?P<pk>\d+)$', DeletePatrullero.as_view(), name='eliminar_patrullero'),
                       )
