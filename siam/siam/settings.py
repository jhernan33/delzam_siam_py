"""
Django settings for siam project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import environ

# environ settings
env = environ.Env()
environ.Env.read_env()

DIR = os.path.abspath(os.path.dirname(__file__))
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8+7n%x=8ccd(*e+nw5ms$6aek*ji1y81@30z#2**y$62!_cn^='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# USE_X_FORWARDED_HOST = True
# Add to project/settings.py
SECURE_HSTS_SECONDS = 30  # Unit is seconds; *USE A SMALL VALUE FOR TESTING!*
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO','https')
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True



MY_PROTOCOL = "https"

# # Add to project/settings.py
# SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_gis',
    'corsheaders',
    'asiam',
    # 'oauth2_provider',
    'django_extensions',
    'django_seed',
    'django_filters',
]

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        'rest_framework.permissions.IsAdminUser'
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

MIDDLEWARE = [
    # Para que CORS funcione bien debe estar lo mas alto, simpre sobre django.middleware.common.CommonMiddleware
    # 'asiam.middleware.PruebaMiddleware',
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'siam.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'siam.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    },
    'comun': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'OPTIONS': {
            'options': '-c search_path=comun'
        },
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    },
    'p2021': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'options': '-c search_path=p2021'
        },
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    },
    'p2022': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'options': '-c search_path=p2022'
        },
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    },
    'empr': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'OPTIONS': {
            'options': '-c search_path=empr'
        },            
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    },    
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
#LANGUAGE_CODE = 'es-ve'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'



# OAUTH2_PROVIDER = {
#     'SCOPES': {'read': 'Read scope', 'write': 'Write scope'}
# }

# If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
# CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# If this is used, then not need to use `CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    # "https://delzam.com.ve/",
    # "https://delzam.com.ve/api/",
    # "https://159.223.168.118/api/",
    # "https://159.223.168.118:8083",
]

# CORS_ORIGIN_WHITELIST = [
#     # "https://delzam.com.ve/"
#     # "https://delzam.com.ve/apidz/"
# ] # Es igual a CORS_ALLOWED_ORIGINS, pero tiene menos prioridad

CORS_TRUSTED_ORIGINS = []



CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "Methods",
    "X-Auth-Token",
    #"access-control-allow-origin",
    #"access-control-allow-headers",
    #"access-control-allow-methods",
]

# CORS_ALLOWED_ORIGIN_REGEXESUna lista de cadenas que representan expresiones regulares que coinciden con los orígenes que están 
#autorizados para realizar solicitudes HTTP entre sitios. El valor predeterminado es [].
#Útil cuando CORS_ALLOWED_ORIGINSno es práctico, como cuando tiene una gran cantidad de subdominios.
#CORS_ORIGIN_REGEX_WHITELIST, que todavía funciona como un alias, y el nuevo nombre tiene prioridad.
#Ejemplo:
#CORS_ALLOWED_ORIGIN_REGEXES  = [
#     r"^https://\w+\.example\.com$" ,
#]

CORS_ALLOWED_ORIGIN_REGEXES = [
    # r"^https://\w+\.delzam\.co.ve$",
]

DEFAULT_AUTO_FIELD =  'django.db.models.BigAutoField'

# LOGGING = {
#     'disable_existing_loggers': False,
#     'version': 1,
#     'handlers': {
#         'console': {
#             # logging handler that outputs log messages to terminal
#             'class': 'logging.StreamHandler',
#             'level': 'DEBUG', # message level to be written to console
#         },
#     },
#     'loggers': {
#         '': {
#             # this sets root level logger to log debug and higher level
#             # logs to console. All other loggers inherit settings from
#             # root level logger.
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': False, # this tells logger to send logging message
#                                 # to its parent (will send if set to True)
#         },
#         'django.db': {
#             # django also has database level logging
#             'level': 'DEBUG'
#         },
#     },
# }

MEDIA_ROOT = os.path.join(DIR,'media')

MEDIA_URL = '/media/'
WEBSERVER_ARTICLE   = '/article/'
WEBSERVER_CUSTOMER  = '/customer/'
WEBSERVER_SELLER    = '/seller/'
WEBSERVER_SUPPLIER  = '/supplier/'
WEBSERVER_LEGAL     = '/legal/'
WEBSERVER_ORDER     = '/order/'
WEBSERVER_BANK      = '/bank/'
WEBSERVER_USER      = '/user/'
WEBSERVER_PORT      =':8083'
WEBSERVER_HOST      ='159.223.168.118'
WEBSERVER_PROTOCOL='https://'
WEBSERVER_API='/api'
WEBSERVER_IMAGES = WEBSERVER_PROTOCOL+WEBSERVER_HOST+WEBSERVER_PORT+WEBSERVER_API+MEDIA_URL
API_PREFIX ='apidz'

UPLOAD_FILES = '/home/delzam/delzam_siam_py/siam/siam/media'