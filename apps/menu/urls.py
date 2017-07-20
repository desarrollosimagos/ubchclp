from django.conf.urls import patterns
from .views import inicio

urlpatterns = patterns('',
                       (r'^', inicio.as_view(template_name="base/base.html")),
                       )
