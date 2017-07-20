#encoding:utf-8
from __future__ import absolute_import
"""
Django settings for ubch project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

RUTA_TEMPLATES = os.path.join(BASE_DIR, 'templates')

TEMPLATE_DIRS = (RUTA_TEMPLATES,)

MEDIA_PDF = os.path.join(BASE_DIR, 'reporte')
REPORTE = '/reporte/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mxj5!wiz)ncm&p!g+w@h3=z@9%^z$bsvsq)vc4@47ay7zsayv8'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = False
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'pixelfields_smart_selects',
    'django_extensions',
    'apps.registro',
    'apps.registro_ubch',
    'apps.patrulleros',
    'apps.clp_ubch',
    'apps.clp',
    'apps.login',
    'apps.topologia.estados',
    'apps.topologia.municipios',
    'apps.topologia.parroquias',
    'apps.centro_votacion',
    'apps.p_bitacora',
    'apps.j_bitacora',
    'apps.c_bitacora',
    'apps.institucion',
    'apps.datos',
    'apps.unodiezinti',


)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',

)

ROOT_URLCONF = 'ubch.urls'

WSGI_APPLICATION = 'ubch.wsgi.application'

#CORS_ALLOW_METHODS = ('GET', 'OPTIONS',)

#CORS_ORIGIN_ALLOW_ALL = True
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ubch',
        'USER': 'ubch',
        'PASSWORD': 'U8cH2015',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Configuraciones de rest framework
REST_FRAMEWORK = {  # Filtrado

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es-VE'

TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = '/home/administrador/django/ubchclp/static/'
STATIC_URL ='http://www.registro1x10.org.ve/static/'

#STATIC_URL = '/static/'

RUTA_STATIC = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (RUTA_STATIC,)

MEDIA_ROOT = os.path.join(BASE_DIR, 'imagenes')
MEDIA_URL = '/imagenes/'

CORS_ORIGIN_ALLOW_ALL = True

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

#REST_FRAMEWORK = {
#    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
#}
