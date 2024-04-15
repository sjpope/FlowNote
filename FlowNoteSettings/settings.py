import os
from dotenv import load_dotenv
from pathlib import Path
from django.urls import reverse_lazy
import dj_database_url
load_dotenv()

# CELERY_BROKER_URL = 'redis://localhost:6379/0' # Celery is using 'Redis' as broker
# REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379')
LOGIN_URL = 'notes:login'
LOGIN_REDIRECT_URL = reverse_lazy('notes:profile')
LOGOUT_REDIRECT_URL = '/'

SITE_ID = 1

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'  
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = os.environ.get('DEBUG') == 'True'

ALLOWED_HOSTS = ['flownote-6d0dd88b2f1f.herokuapp.com', 'localhost', '127.0.0.1']

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT'))  
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS') # == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# Application definition
INSTALLED_APPS = [
    # Django Apps
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
    'channels',
    'ckeditor',
    # 'django_celery_results',
    # 'django_q',
    # Internal Apps
    'notes',
    'AIEngine',
    
]


# Q_CLUSTER = {
#     'name': 'DjangORM',
#     'workers': 4,
#     'timeout': 90,
#     'retry': 120,
#     'queue_limit': 50,
#     'bulk': 10,
#     'orm': 'default',
# }

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

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

ASGI_APPLICATION = 'FlowNoteSettings.asgi.application'
WSGI_APPLICATION = 'FlowNoteSettings.wsgi.application'

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [REDIS_URL],
#         },
#     },
# }


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

# AUTH_USER_MODEL = 'notes.UserProfile'

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
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'fonts', 'items': ['Font', 'FontSize']},
            {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent']},
            {'name': 'links', 'items': ['Link', 'Unlink']},
            {'name': 'tools', 'items': ['RemoveFormat', 'Source']},
        ],
        'extraAllowedContent': 'span{background,color};',
        'removePlugins': 'elementspath',
    }
}