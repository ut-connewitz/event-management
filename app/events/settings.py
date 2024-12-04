"""
Django settings for events project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import json
import os
from pathlib import Path
from celery.schedules import crontab
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
CSRF_TRUSTED_ORIGINS = json.loads(os.getenv('CSRF_TRUSTED_ORIGINS', '[]'))

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'django_celery_beat',
    'django_bootstrap5',
    'dark_mode_switch',
    'backend', # this has to be above 'django.contrib.admin' to ovewrite default admin panel styling
    'events_calendar',
    'profile_page',
    'django.contrib.admin', # this has to be below 'backend' otherwise default admin panel styles will be used
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'events.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'events.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}


AUTH_USER_MODEL = 'backend.User'

# change back to default ('accounts/profile'/) once its implemented
LOGIN_REDIRECT_URL = '/ecal/calendar/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# https://docs.djangoproject.com/en/4.2/topics/email/#smtp-backend
# necessary settings for sending emails from the django app
# for development, we can just print the emails to the console:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# for production use the following pattern and set the variables in the .env file
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = $EMAIL_HOST #tbd
# EMAIL_PORT = $EMAIL_PORT #tbd
# EMAIL_USE_TLS = True #tbd
# EMAIL_HOST_USER = $EMAIL_HOST_USER #tbd
# EMAIL_HOST_PASSWORD = $EMAIL_HOST_PASSWORD #tbd

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'de-DE'

TIME_ZONE = 'Europe/Berlin'

TIME_FORMAT = 'H:i'

TIME_INPUT_FORMATS = [
    '%H:%M',
]

DATE_FORMAT = 'd.m.Y'

DATE_INPUT_FORMATS = ('%d.%m.%Y', '%d.%m.%y', '%d. %b %Y', '%d. %M %Y',
                      '%d-%m-%Y', '%d/%m/%Y', '%d/%m/%y', '%d %b %Y',
                      '%d %b, %Y', '%d %b %Y', '%d %b, %Y', '%d %B, %Y',
                      '%d %B %Y')

DATETIME_FORMAT = 'd.m.Y, H:i'

DATETIME_INPUT_FORMATS = ('%d.%m.%Y %H:%M', '%d.%m.%y %H:%M', '%d. %b %Y %H:%M', '%d. %M %Y %H:%M',
                          '%d.%m.%Y', '%d.%m.%y', '%d.%b.%Y', '%d.%M.%Y',
                          '%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%d/%m/%Y',
                          '%d/%m/%y %H:%M:%S', '%d/%m/%y %H:%M', '%d/%m/%y',
                          '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d')

USE_I18N = True

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/static/'
MEDIA_URL = '/static/media/'

STATIC_ROOT = '/vol/web/static'
MEDIA_ROOT = '/vol/web/media'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# custom logger
LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[DJANGO] %(levelname)s %(asctime)s %(module)s '
                          '%(name)s.%(funcName)s:%(lineno)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
            'celery': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '/var/log/celery/events.log',
                'formatter': 'default',
                'maxBytes': 1024 * 1024 * 5,
                'backupCount': 3,
            }
        },
        'loggers': {
            '*': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'celery': {
                'handlers': ['celery', 'console'],
                'level': 'INFO'
            },
        },
    }

# celery settings
CELERY_HIJACK_ROOT_LOGGER = False
CELERY_SEND_EVENTS = False
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_RESULT_PERSISTENT = False
CELERY_TIMEZONE = 'Europe/Berlin'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30*60
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BEAT_SCHEDULE = {
#    'add':{
#    'schedule': 30.0,
#    'args': (16, 16)
#    },

    #remove this or comment out for deploy
#    'delete_past_events_test':{
#        'task': 'events.celery_tasks.delete_past_events',
#        'schedule': 30.0,
#    },

    'delete_past_events_daily':{
        'task': 'events.celery_tasks.delete_past_events',
        'schedule': crontab(hour='3', minute='0'),
    },
}
