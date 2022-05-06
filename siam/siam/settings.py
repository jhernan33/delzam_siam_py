"""
Django settings for siam project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8+7n%x=8ccd(*e+nw5ms$6aek*ji1y81@30z#2**y$62!_cn^='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'asiam',
    'oauth2_provider',
    'corsheaders',
    'django_extensions',
    'django_seed',
    'rest_framework_gis',
]

MIDDLEWARE = [
    # Para que CORS funcione bien debe estar lo mas alto, simpre sobre django.middleware.common.CommonMiddleware
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'siam.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_delzam_py',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': '159.223.168.118',
        'PORT': '5432',
    },
    'comun': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'options': '-c search_path=comun'
        },            
        'NAME': 'db_delzam_py',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': '159.223.168.118',
        'PORT': '5432',
    },
    'p2021': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'options': '-c search_path=p2021'
        },            
        'NAME': 'db_delzam_py',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': '159.223.168.118',
        'PORT': '5432',
    },
    'p2022': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'options': '-c search_path=p2022'
        },            
        'NAME': 'db_delzam_py',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': '159.223.168.118',
        'PORT': '5432',
    },
    'empr': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'options': '-c search_path=empr'
        },            
        'NAME': 'db_delzam_py',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': '159.223.168.118',
        'PORT': '5432',
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

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
     'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )

}

OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope'}
}

# If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = False

# If this is used, then not need to use `CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://159.223.168.118:8082"
]

CORS_ORIGIN_WHITELIST = [] # Es igual a CORS_ALLOWED_ORIGINS, pero tiene menos prioridad

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

CORS_ALLOWED_ORIGIN_REGEXES = []

DEFAULT_AUTO_FIELD =  'django.db.models.BigAutoField'