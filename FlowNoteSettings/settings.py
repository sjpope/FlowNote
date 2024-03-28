import os
from dotenv import load_dotenv
from pathlib import Path
from django.urls import reverse_lazy
import dj_database_url
load_dotenv()

CELERY_BROKER_URL = 'redis://localhost:6379/0' # Celery is using 'Redis' as broker

LOGIN_URL = 'notes:login'
LOGIN_REDIRECT_URL = reverse_lazy('notes:profile')
LOGOUT_REDIRECT_URL = '/'

SITE_ID = 1

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'  
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # 'notes/static'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Dev Settings - unsuitable for production https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = True

ALLOWED_HOSTS = ['flownote.herokuapp.com', 'localhost', '127.0.0.1']
# ALLOWED_HOSTS = []

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT'))  
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS') # == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #'allauth.account.models.EmailAddress',
    
    'rest_framework',
    'notes',
    'AIEngine',
    'DataConnector',
]

MIDDLEWARE = [
    # Use the Associated Middleware Stack instead.
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'allauth.account.middleware.AccountMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'FlowNoteSettings.urls'

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

WSGI_APPLICATION = 'FlowNoteSettings.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3', conn_max_age=600),
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.environ.get('DB1_PATH', BASE_DIR / 'db.sqlite3'),
    # },
    'mssql': {
        'ENGINE': 'mssql',
        'NAME': os.environ.get('MSSQL_DB_NAME'),
        'USER': os.environ.get('MSSQL_USER'),
        'PASSWORD': os.environ.get('MSSQL_PASSWORD'),
        'HOST': os.environ.get('MSSQL_HOST'),
        'PORT': os.environ.get('MSSQL_PORT'),

        'OPTIONS': {
            'driver': os.environ.get('MSSQL_DRIVER'),
        },
    },
    'mongodb': {
        'ENGINE': 'djongo',
        'NAME': os.environ.get('MONGO_DB_NAME'),
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': os.environ.get('MONGO_URI'),
        }
    }
}

# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
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

# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""
Django settings for app project.
Generated by 'django-admin startproject' using Django 5.0.2.
For more information on this file, see https://docs.djangoproject.com/en/5.0/topics/settings/
For the full list of settings and their values, see https://docs.djangoproject.com/en/5.0/ref/settings/
"""