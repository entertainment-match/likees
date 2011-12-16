# coding=utf-8
# Django settings for entertainmentmatch project.
import os
import djcelery
djcelery.setup_loader()

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Admin Name', 'admin@mail.com'),
)

MANAGERS = ADMINS

TEMPLATE_DOMAIN = 'url web'
COVER_DOMAIN = 'http://cf1.themoviedb.org/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'likees_dev',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '4242',
        'TEST_COLLATION': 'uft8_bin',
    },
    'likees_pro': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'likees',                      # Or path to database file if using sqlite3.
        'USER': 'username_pro',                      # Not used with sqlite3.
        'PASSWORD': 'password_pro',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '4242',                      # Set to empty string for default. Not used with sqlite3.
        'TEST_COLLATION' : 'utf8_bin',
    }
}

#DATABASE_ENGINE = 'mysql'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

ugettext = lambda s: s

LANGUAGES = (
    ('en', ugettext('English')),
    ('es', ugettext('Spanish')),
    ('fr', ugettext('French')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

## TODO fcs: falta normalizar el path para todos los entornos
MEDIA_ROOT = '/home/likees/likees/src/entertainmentmatch/likees/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^@nrr4c^2z2&%(nui4$6wnp+d=xc=4tg63lcf83lq$(d!6#a!8'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "socialauth.context_processors.facebook_api_key",
    "likees.context_processors.template_domain",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'likees.middleware.likees_middleware.LikeesMiddleware',
    'likees.middleware.soulmates.SoulmatesMiddleware',
#    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'entertainmentmatch.urls'

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_DOC_ROOT = os.path.join(PROJECT_DIR, "likees/media/")

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, "/likees/templates")
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
#    'django.contrib.messages',
    'django.contrib.admin',
    'entertainmentmatch.likees',
    'entertainmentmatch.rosetta',
    'djcelery',
    
    #'socialauth'
)

LOGIN_REDIRECT_URL = ('/likees/dashboard')
LOGIN_URL = ('/likees/accounts/login')

LOGOUT_URL = ('/likees/')

AUTHENTICATION_BACKENDS = (
    'entertainmentmatch.likees.auth_backends.CustomUserModelBackend',
    #'socialauth.auth_backends.FacebookBackend',
    #'socialauth.auth_backends.TwitterBackend',
)

CUSTOM_USER_MODEL = 'likees.UserLikees'

FACEBOOK_APP_ID = ''
FACEBOOK_API_KEY = ''
FACEBOOK_SECRET_KEY = ''

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

HASH_SALT = 'it5YMSLWbWDQA8S'

NUM_RESULTS = 20
SEARCH_NUM_RESULTS = 10
DASHBOARD_MAX_ITEMS = 10
DASHBOARD_MAX_USERS = 5

LIKEES_ENVIROMENT = os.environ.get('LIKEES_ENVIROMENT', None) 

AVATAR_PATH = '/home/likees/dev/avatar/'

if LIKEES_ENVIROMENT == 'pro':
    from settings_pro import *
    
CRITIC_MIN_LENGHT = 20
SOULMATE_LIMIT = 5
ITEM_DETAIL_MAX_USERS = 12

DEFAULT_USER_LANGUAGE = 'default'
DEFAULT_USER_TIMEZONE = 'gmt+1'
DEFAULT_USER_PUBLISH_EVENTS = 1
DEFAULT_USER_NOTIFY_MAIL = 1
DEFAULT_FACEBOOK_PUBLISH_VOTES = 1
DEFAULT_FACEBOOK_PUBLISH_FAVES= 1

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 5672
BROKER_VHOST = "/rabbit"
BROKER_USER = "rabbitmq"
BROKER_PASSWORD = "r4bb1t"
