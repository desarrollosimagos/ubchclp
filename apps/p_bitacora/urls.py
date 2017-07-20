from django.conf.urls import patterns, url
from views import BitacoraView

urlpatterns = patterns('',
                       url(r'^pdf_bitacora/$', BitacoraView.as_view(), name="bitacora"),
                       )
