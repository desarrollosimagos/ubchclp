from django.conf.urls import patterns, url
from .views import ListDatosView, UpdateDatosView, DetailDatosView, RegistroView, MiListaView, LoginView, ReporteDatosView, UpdateDatosPassView, CreateDatosUserView,  ReportePatrullerosView, ReportePatrullerosJefesView, ReportePatrullerosDetailView, ListPatrullerosView, ListJefesView, ListNoCargaView, ReporteNoCargaView
from django.views.generic import TemplateView
urlpatterns = patterns('',
                       url(r'^registro/$', RegistroView.as_view(),name="registro_datos"),
                       url(r'^listar/$', ListDatosView.as_view(),name="list_datos"),
                       url(r'^update/$', UpdateDatosView.as_view(),name="update_datos"),
                       url(r'^detail/(?P<pk>\d+)/$', DetailDatosView.as_view(),name="detail_datos"),
                       url(r'^milista/$', MiListaView.as_view(),name="milista_datos"),
                       url(r'^detail$', DetailDatosView.as_view(),name="detail_datos"),
                       url(r'^fecha/$', TemplateView.as_view(template_name="datos/fecha.html"), name='fecha'),
                       url(r'^fechalogin/$', LoginView.as_view(template_name="datos/fecha.html"), name='fecha_login'),
                       url(r'^reporte/$', ReporteDatosView.as_view(), name='reporte_datos'),
                       url(r'^actualizar/(?P<pk>\d+)$', UpdateDatosPassView.as_view()),
                       url(r'^crear/(?P<cedula>\d+)$', CreateDatosUserView.as_view()),

                       url(r'^listar_patrulleros/$', ListPatrullerosView.as_view(),name="list_patrulleros"),
                       url(r'^listar_nocargado/$', ListNoCargaView.as_view(),name="list_nocarga"),
                       url(r'^listar_jefes/$', ListJefesView.as_view(),name="list_jefes"),
                       url(r'^reporte_patrulleros/$', ReportePatrullerosView.as_view(), name='reporte_patrulleros'),
                       url(r'^reporte_nocarga/$', ReporteNoCargaView.as_view(), name='reporte_nocarga'),
                       url(r'^reporte_jefes/$', ReportePatrullerosJefesView.as_view(), name='reporte_jefes'),
                       url(r'^reporte_detallado/(?P<pk>\d+)$', ReportePatrullerosDetailView.as_view(), name='reporte_detallado'),
                       )
