import os
import sys
import dj_database_url

WEBAPP_DIR = os.path.dirname(os.path.abspath(__file__))
APP_BASEDIR = os.path.abspath(os.path.join(WEBAPP_DIR, os.path.pardir))

DEBUG = os.getenv('DEBUG_MODE', 'true') == 'true'
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['localhost']

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

MEDIA_ROOT = os.path.join(APP_BASEDIR, 'uploads')
MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(APP_BASEDIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(WEBAPP_DIR, 'static'),)

ROOT_URLCONF = 'etat.urls'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

if 'runserver' in sys.argv:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'etat@gloggi.ch')
SERVER_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'etat@gloggi.ch')

TEMPLATE_DIRS = (
    os.path.join(WEBAPP_DIR, 'templates')
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
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
    'south',
    'mptt',
    'django_mptt_admin',
    'django_reset',
    'django_countries',
    'django_filters',
    'django_select2',
    'rest_framework',
    'bootstrapform',
    'sorl.thumbnail',

    'etat',
    'etat.departments',
    'etat.members',
)

SUIT_CONFIG = {
    'ADMIN_NAME': 'Etat Admin',
    'SEARCH_URL': 'admin:members_member_changelist',
    'MENU_ICONS': {
        'departments': 'icon-folder-open',
        'members': 'icon-user',
    }
}
