# coding=utf-8
# Django settings for development branch.
DEBUG = False

TEMPLATE_DOMAIN = 'http://www.likees.org/'

AVATAR_PATH = '/home/likees/pro/avatar/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'likees',                      # Or path to database file if using sqlite3.
        'USER': 'username',                      # Not used with sqlite3.
        'PASSWORD': 'password',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '4242',                      # Set to empty string for default. Not used with sqlite3.
        'TEST_COLLATION' : 'utf8_bin',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
#    'django.contrib.messages',
    'django.contrib.admin',
    'entertainmentmatch.likees',
    'djcelery',
    #'socialauth'
)

DEFAULT_USER_NOTIFY_MAIL = 1
