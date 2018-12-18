# vim: set fileencoding=utf-8
# this system uses structured settings as defined in
# http://www.slideshare.net/jacobian/the-best-and-worst-of-django
#
# this is the base settings.py -- which contains settings common to all
# implementations of ona: edit it at last resort
#
# local customizations should be done in several files each of which in turn
# imports this one.
# The local files should be used as the value for your DJANGO_SETTINGS_FILE
# environment variable as needed.
import logging
import os
import subprocess  # nopep8, used by included files
import sys  # nopep8, used by included files

from celery.signals import after_setup_logger
from django.core.exceptions import SuspiciousOperation
from django.utils.log import AdminEmailHandler
import djcelery
from pymongo import MongoClient


djcelery.setup_loader()

CURRENT_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.realpath(
    os.path.join(os.path.dirname(CURRENT_FILE), '..//'))
PRINT_EXCEPTION = False

TEMPLATED_EMAIL_TEMPLATE_DIR = 'templated_email/'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

#show metadata in exported files flag
SHOW_EXPORT_METADATA = True


DEFAULT_FROM_EMAIL = 'noreply@ona.io'
SHARE_PROJECT_SUBJECT = '{} Ona Project has been shared with you.'
DEFAULT_SESSION_EXPIRY_TIME = 21600  # 6 hours

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'
#ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(' ')


# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

ugettext = lambda s: s

LANGUAGES = (
    ('fr', u'Français'),
    ('en', u'English'),
    ('es', u'Español'),
    ('it', u'Italiano'),
    ('km', u'ភាសាខ្មែរ'),
    ('ne', u'नेपाली'),
    ('nl', u'Nederlands'),
    ('zh', u'中文'),
)

SITE_ID = 2

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://newdawn.mpower-social.com:8001/media/'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Enketo URL.
# Constants.
ENKETO_API_ENDPOINT_ONLINE_SURVEYS = '/survey'
ENKETO_API_ENDPOINT_OFFLINE_SURVEYS = '/survey/offline'
ENKETO_API_ENDPOINT_INSTANCE= '/instance'
ENKETO_API_ENDPOINT_INSTANCE_IFRAME= '/instance/iframe'
# Configurable settings.
ENKETO_API_TOKEN = os.environ.get('ENKETO_API_TOKEN', 'enketorules')
ENKETO_URL = os.environ.get('ENKETO_URL', 'https://enketo.kobotoolbox.org')
print '**********************************************************************'
print ENKETO_URL
ENKETO_API_ROOT= os.environ.get('ENKETO_API_ROOT') or os.environ.get('ENKETO_API_URL_PARTIAL') or '/api_v1' # TODO: Remove backward compatibility with "ENKETO_API_URL_PARTIAL".
ENKETO_API_ENDPOINT_PREVIEW= os.environ.get('ENKETO_API_ENDPOINT_PREVIEW') or os.environ.get('ENKETO_PREVIEW_URL_PARTIAL') or '/webform/preview' # TODO: Remove backward compatibility with "ENKETO_PREVIEW_URL_PARTIAL".
ENKETO_OFFLINE_SURVEYS= ('/api/v2' in ENKETO_API_ROOT) and \
        (os.environ.get('ENKETO_OFFLINE_SURVEYS', '').lower() == 'true') # Offline surveys are only possible in API v2.
ENKETO_API_ENDPOINT_SURVEYS= ENKETO_API_ENDPOINT_OFFLINE_SURVEYS if ENKETO_OFFLINE_SURVEYS \
        else ENKETO_API_ENDPOINT_ONLINE_SURVEYS

ENKETO_API_SURVEY_PATH = ENKETO_API_ROOT + ENKETO_API_ENDPOINT_SURVEYS
ENKETO_API_INSTANCE_PATH = ENKETO_API_ROOT + ENKETO_API_ENDPOINT_INSTANCE
ENKETO_PREVIEW_URL = ENKETO_URL + ENKETO_API_ENDPOINT_PREVIEW
ENKETO_API_INSTANCE_IFRAME_URL = ENKETO_URL + ENKETO_API_ROOT + ENKETO_API_ENDPOINT_INSTANCE_IFRAME

# specifically for site urls sent to enketo
ENKETO_PROTOCOL = os.environ.get('ENKETO_PROTOCOL', 'https')

# Login URLs
#LOGIN_URL = '/accounts/login/'
#LOGIN_REDIRECT_URL = '/login_redirect/'
LOGIN_URL = '/usermodule/login/'
LOGIN_REDIRECT_URL = '/usermodule/login/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'readonly.context_processors.readonly',
    'onadata.apps.main.context_processors.google_analytics',
    'onadata.apps.main.context_processors.site_name',
    'onadata.apps.main.context_processors.base_url',
    'onadata.apps.usermodule.context_processors.additional_menu_items',
    'onadata.apps.usermodule.context_processors.is_admin',
    'onadata.apps.usermodule.context_processors.care_viewer',
)

MIDDLEWARE_CLASSES = (
    'reversion.middleware.RevisionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'onadata.libs.utils.middleware.LocaleMiddlewareWithTweaks',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'onadata.libs.utils.middleware.HTTPResponseNotAllowedMiddleware',
    'readonly.middleware.DatabaseReadOnlyMiddleware',
)

LOCALE_PATHS = (os.path.join(PROJECT_ROOT, 'onadata.apps.main', 'locale'), )

ROOT_URLCONF = 'onadata.apps.main.urls'
USE_TZ = False
ALLOWED_HOSTS = '*'
USE_L10N = False

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'libs/templates'),
    os.path.join(PROJECT_ROOT, 'apps/care_reports/templates/report'),
    # Put strings here, like "/home/html/django_templates"
    # or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# needed by guardian
ANONYMOUS_USER_ID = -1

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.gis',
    'registration',
    'south',
    'reversion',
    'django_nose',
    'django_digest',
    'corsheaders',
    'oauth2_provider',
    'rest_framework',
    'rest_framework.authtoken',
    'taggit',
    'readonly',
    'onadata.apps.logger',
    'onadata.apps.viewer',
    'onadata.apps.main',
    'onadata.apps.scheduling',
    'onadata.apps.approval',
    'onadata.apps.restservice',
    'onadata.apps.api',
    'guardian',
    'djcelery',
    'onadata.apps.stats',
    'onadata.apps.sms_support',
    'onadata.libs',
    'onadata.apps.unicef',
    'onadata.apps.usermodule',
    'onadata.apps.dashboard',
    'onadata.apps.dashboard_tool',
    #'highcharts',
    'onadata.apps.audit_log',
    'crispy_forms',
    'onadata.apps.bgmodule',
    'onadata.apps.fao_module',
)

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'groups': 'Access to your groups'}
}

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
    'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'onadata.libs.authentication.DigestAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.UnicodeJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONPRenderer',
        'rest_framework.renderers.XMLRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
    ),
    'VIEW_NAME_FUNCTION': 'onadata.apps.api.tools.get_view_name',
    'VIEW_DESCRIPTION_FUNCTION': 'onadata.apps.api.tools.get_view_description',
}

SWAGGER_SETTINGS = {
    "exclude_namespaces": [],    # List URL namespaces to ignore
    "api_version": '1.0',  # Specify your API's version (optional)
    "enabled_methods": [         # Methods to enable in UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
}

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'dev.ona.io',
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

USE_THOUSAND_SEPARATOR = True

COMPRESS = True

# extra data stored with users
AUTH_PROFILE_MODULE = 'onadata.apps.main.UserProfile'

# case insensitive usernames -- DISABLED for KoBoForm compatibility
AUTHENTICATION_BACKENDS = (
    #'onadata.apps.main.backends.ModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# Settings for Django Registration
ACCOUNT_ACTIVATION_DAYS = 1


def skip_suspicious_operations(record):
    """Prevent django from sending 500 error
    email notifications for SuspiciousOperation
    events, since they are not true server errors,
    especially when related to the ALLOWED_HOSTS
    configuration

    background and more information:
    http://www.tiwoc.de/blog/2013/03/django-prevent-email-notification-on-susp\
    iciousoperation/
    """
    if record.exc_info:
        exc_value = record.exc_info[1]
        if isinstance(exc_value, SuspiciousOperation):
            return False
    return True

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s' +
                      ' %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        # Define filter for suspicious urls
        'skip_suspicious_operations': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_suspicious_operations,
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', 'skip_suspicious_operations'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout
        },
        'audit': {
            'level': 'DEBUG',
            'class': 'onadata.libs.utils.log.AuditLogHandler',
            'formatter': 'verbose',
            'model': 'onadata.apps.main.models.audit.AuditLog'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'console_logger': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'audit_logger': {
            'handlers': ['audit'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}


def configure_logging(logger, **kwargs):
    admin_email_handler = AdminEmailHandler()
    admin_email_handler.setLevel(logging.ERROR)
    logger.addHandler(admin_email_handler)

after_setup_logger.connect(configure_logging)

MONGO_DATABASE = {
    'HOST': '192.168.19.19',
    'PORT': 27017,
    'NAME': 'fao',
    'USER': '',
    'PASSWORD': ''
}

GOOGLE_STEP2_URI = 'http://ona.io/gwelcome'
GOOGLE_CLIENT_ID = '617113120802.onadata.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '9reM29qpGFPyI8TBuB54Z4fk'

THUMB_CONF = {
    'large': {'size': 1280, 'suffix': '-large'},
    'medium': {'size': 640, 'suffix': '-medium'},
    'small': {'size': 240, 'suffix': '-small'},
}
# order of thumbnails from largest to smallest
THUMB_ORDER = ['large', 'medium', 'small']
IMG_FILE_TYPE = 'jpg'

# celery
BROKER_BACKEND = "librabbitmq"
BROKER_URL = 'amqp://guest:guest@localhost:5672/'
CELERY_RESULT_BACKEND = "amqp"  # telling Celery to report results to RabbitMQ
CELERY_ALWAYS_EAGER = False

# duration to keep zip exports before deletion (in seconds)
ZIP_EXPORT_COUNTDOWN = 3600  # 1 hour

# default content length for submission requests
DEFAULT_CONTENT_LENGTH = 10000000

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--with-fixture-bundling']

# fake endpoints for testing
TEST_HTTP_HOST = 'testserver.com'
TEST_USERNAME = 'bob'

# re-captcha in registrations
REGISTRATION_REQUIRE_CAPTCHA = False
RECAPTCHA_USE_SSL = False
RECAPTCHA_PRIVATE_KEY = ''
RECAPTCHA_PUBLIC_KEY = '6Ld52OMSAAAAAJJ4W-0TFDTgbznnWWFf0XuOSaB6'

# specify the root folder which may contain a templates folder and a static
# folder used to override templates for site specific details
TEMPLATE_OVERRIDE_ROOT_DIR = None

# Use 1 or 0 for multiple selects instead of True or False for csv, xls exports
BINARY_SELECT_MULTIPLES = False

# Use 'n/a' for empty values by default on csv exports
NA_REP = 'n/a'

# MongoDB
if MONGO_DATABASE.get('USER') and MONGO_DATABASE.get('PASSWORD'):
    MONGO_CONNECTION_URL = (
        "mongodb://%(USER)s:%(PASSWORD)s@%(HOST)s:%(PORT)s") % MONGO_DATABASE
else:
    MONGO_CONNECTION_URL = "mongodb://%(HOST)s:%(PORT)s" % MONGO_DATABASE

MONGO_CONNECTION = MongoClient(
    MONGO_CONNECTION_URL, safe=True, j=True, tz_aware=True)
MONGO_DB = MONGO_CONNECTION[MONGO_DATABASE['NAME']]

# Set wsgi url scheme to HTTPS
os.environ['wsgi.url_scheme'] = 'https'

SUPPORTED_MEDIA_UPLOAD_TYPES = [
    'image/jpeg',
    'image/png',
    'audio/mpeg',
    'video/3gpp',
    'video/mp4',
    'video/ogg',
    'audio/wav',
    'audio/x-m4a',
    'audio/mp3',
    'text/csv',
    'text/html',
    'application/zip'
]

# legacy setting for old sites who still use a local_settings.py file and have
# not updated to presets/
try:
    from local_settings import *  # nopep8
except ImportError:
    pass

if isinstance(TEMPLATE_OVERRIDE_ROOT_DIR, basestring):
    # site templates overrides
    TEMPLATE_DIRS = (
        os.path.join(PROJECT_ROOT, TEMPLATE_OVERRIDE_ROOT_DIR, 'templates'),
    ) + TEMPLATE_DIRS
    # site static files path
    STATICFILES_DIRS += (
        os.path.join(PROJECT_ROOT, TEMPLATE_OVERRIDE_ROOT_DIR, 'static'),
    )

EMAIL_HOST = 'smtp.office365.com'

EMAIL_HOST_USER = 'ratna@mpower-social.com'

EMAIL_HOST_PASSWORD = ''

EMAIL_PORT = 587

EMAIL_USE_TLS = True

