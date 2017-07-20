from django.conf.urls import patterns, url
from .views import ListDatosView, UpdateDatosView, DetailDatosView, RegistroView, MiListaView, LoginView, ReporteDatosView, UpdateDatosPassView, CreateDatosUserView
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
                       )
