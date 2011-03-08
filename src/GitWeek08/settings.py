# Django settings for recipesite project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Melissa','melissafmtek@gmail.com'),
)   

MANAGERS = ADMINS

INTERNAL_IPS = ('127.0.0.1','71.112.208.102')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dtest',
        'USER': 'djuser',
        'PASSWORD': 'pgadmin',
        'HOST': 'localhost', 
        'PORT': '3306',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Vancouver'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold static application files
# such as css or non-template html or jpg and other image files. Use a trailing slash.
# Don't use the same path as for admin media.
MEDIA_ROOT = '/home/mlrice/www/static/'  #absolute path to media


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
MEDIA_URL = '/static/' #because admin already using /media

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# alias to where admin media lives?? e.g. ?/django/contrib/admin/media
# Examples: "http://foo.com/media/", "/media/".
# The URL prefix for admin media -- CSS, JavaScript and images used by the 
# Django administrative interface. Make sure to use a trailing slash, and 
# to have this be different from the MEDIA_URL setting (since the same URL 
# cannot be mapped onto two different sets of files).
ADMIN_MEDIA_PREFIX = 'http://block115397-xwp.blueboxgrid.com/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&&%ct--va80v7p+c44uh2h+hvnr=0#_^0i2zb6j2x_i#6c=t0b'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'dtest.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/mlrice/www/dtest/templates/'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    # 'south',
    'debug_toolbar',
    'recipes',
    #'menus',
)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

