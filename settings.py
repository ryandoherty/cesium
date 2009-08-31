import os

# Use `path` to talk about directories relative to this file.
ROOT = os.path.abspath(os.path.dirname(__file__))
path = lambda *paths: os.path.join(ROOT, *paths)


### The following MUST be overridden in local_settings.py ###

DEBUG = False 
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS

# 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_ENGINE = ''
# Or path to database file if using sqlite3.
DATABASE_NAME = ''
# Not used with sqlite3.
DATABASE_USER = ''
# Not used with sqlite3.
DATABASE_PASSWORD = ''
# Set to empty string for localhost. Not used with sqlite3.
DATABASE_HOST = ''
# Set to empty string for default. Not used with sqlite3.
DATABASE_PORT = ''
# Options for the database
DATABASE_OPTIONS = {
    # MySQL Specific -- override locally if not using MySQL
    "init_command": "SET storage_engine=INNODB",
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

### Sensible defaults that MAY need be overridden in local_settings.py ###

TIME_ZONE = 'America/Los_Angeles'

MEDIA_ROOT = path('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

TEMPLATE_DIRS = (
    path('templates')
)

# This is the port the scheduling daemon will run on.
AUTOYSLOW_DAEMON_PORT = 8003
LOADS_PER_PROC = 10
PAGE_TIMEOUT = 15    # Per web page.

# Full path to the Firefox executable.
BROWSER_LOC = ''

### Probably don't need to override anything under here. ###

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'cesium.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'cesium.south',
    'cesium.autoyslow'
)

LOGIN_REDIRECT_URL = '/'

try:
    from local_settings import *
except ImportError:
    pass
