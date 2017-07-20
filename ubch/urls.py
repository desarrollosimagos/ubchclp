from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings


urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('apps.login.urls')),
                       url(r'^ubch/', include('apps.registro.urls')),
                       url(r'^ubch/', include('apps.registro_ubch.urls')),
                       url(r'^clp/', include('apps.clp.urls')),
                       url(r'^', include('apps.login.urls')),
                       url(r'^menu/$', include('apps.menu.urls')),
                       url(r'^estado/', include('apps.topologia.estados.urls')),
                       url(r'^municipio/',
                           include('apps.topologia.municipios.urls')
                           ),
                       url(r'^parroquia/',
                           include('apps.topologia.parroquias.urls')
                           ),
                       url(r'^clpubch/',
                           include('apps.clp_ubch.urls')
                           ),
                       url(r'^patrullero/',
                           include('apps.patrulleros.urls')
                           ),
                       url(r'^reporte/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_PDF}),
                       url(r'^datos/', include('apps.datos.urls')),
                       )


