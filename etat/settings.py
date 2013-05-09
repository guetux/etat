import os
import sys
import dj_database_url
from memcacheify import memcacheify

WEBAPP_DIR = os.path.dirname(os.path.abspath(__file__))
APP_BASEDIR = os.path.abspath(os.path.join(WEBAPP_DIR, os.path.pardir))

DEBUG = os.getenv('DEBUG_MODE', 'true') == 'true'
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['localhost', '.herokuapp.com', '.heroku.feinheit.ch']

ADMINS = (
    ('Stefan Reinhard / Chili', 'chili@gloggi.ch'),
)

MANAGERS = ADMINS

SECRET_KEY = os.environ.get('SECRET_KEY', 'unsecure_dummy')

# Parse database configuration from $DATABASE_URL
DEV_DB = os.path.join(APP_BASEDIR, 'dev.db')
DATABASES = {'default': dj_database_url.config(default='sqlite:///%s' % DEV_DB)}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

TIME_ZONE = 'Europe/Zurich'

_ = lambda s: s

LANGUAGE_CODE = 'de'

LANGUAGES = (
    ('de', _('German')),
    ('en', _('English')),
)

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

MEDIA_ROOT = os.path.join(APP_BASEDIR, 'uploads')
MEDIA_URL = '/uploads/'

if 'runserver' not in sys.argv:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

STATIC_ROOT = os.path.join(APP_BASEDIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(WEBAPP_DIR, 'static'),)

ROOT_URLCONF = 'etat.urls'

CACHES = memcacheify()

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

if 'runserver' in sys.argv:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_HOST = os.environ.get('MAILGUN_SMTP_SERVER')
    EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN')
    EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD')
    EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT', 587)
    EMAIL_USE_TLS = True


DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'etat@gloggi.ch')
SERVER_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'etat@gloggi.ch')

TEMPLATE_DIRS = (
    os.path.join(WEBAPP_DIR, 'templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

INSTALLED_APPS = (
    'suit',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'raven.contrib.django.raven_compat',
    'storages',
    'south',
    'mptt',
    'django_reset',
    'django_countries',

    'etat',
    'etat.departments',
    'etat.members',
)

SUIT_CONFIG = {
    'ADMIN_NAME': 'Etat Admin'
}