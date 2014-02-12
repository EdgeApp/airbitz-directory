"""
Django settings for airbitz project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_HOST = 'localhost'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vjhh1t5!3t69w%ytjq5+@u12hh)(qme(&kkxzdmf%gy*&x4cur'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []
GOOGLE_MAP_KEY = 'AIzaSyAfLR1iSlX6422D6huTncZWn5LIh2-HcVU'

FS_CLIENT_ID='JYRB30J3V1EVKVTIKFOZQ1NZ4Z5CVL2WYCJUEIBABTDFIHFJ'
FS_CLIENT_SECRET='HQCHFV2B5SPZUUPTADYHYZRYNYZH0NG4LM3FUKNWFSP0UU4Y'

# Application definition
SITE_ROOT = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, "templates"),
    os.path.join(SITE_ROOT, "templates/site"),
)
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.gis',
    'haystack',
    'imagekit',
    'pipeline',
    'crispy_forms',
    'rest_framework',
    'south',

    'restapi',
    'location',
    'directory',
    'management',
)
if DEBUG:
    INSTALLED_APPS += (
        'rest_framework_swagger',
    )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    'django.core.context_processors.request',
    "django.contrib.messages.context_processors.messages",
    'airbitz.processors.near',
)

ROOT_URLCONF = 'airbitz.urls'

WSGI_APPLICATION = 'airbitz.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'airbitz_directory',
        'USER': 'airbitz',
        'PASSWORD': 'airbitz',
        'HOST': DB_HOST,
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
if DEBUG:
    MEDIA_ROOT = os.path.join(os.environ['HOME'], 'media')
    MEDIA_URL = '/media/'
else:
    MEDIA_ROOT = os.path.join(os.environ['HOME'], 'media')
    MEDIA_URL = 'http://www.airbitz.co/media/'


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.environ['HOME'], 'static')
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static/'),
)
PIPELINE_CSS = {
    'global': {
        'source_filenames': (
            'bootstrap/css/bootstrap.css',
            'css/global-stylesheet.css',
        ),
        'output_filename': 'css/global.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'management': {
        'source_filenames': (
            'extras/select2/select2.css',
        ),
        'output_filename': 'css/management.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'dataTables': {
        'source_filenames': (
            'extras/DataTables-1.9.4/media/css/jquery.dataTables.css',
        ),
        'output_filename': 'css/dataTables.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
}
PIPELINE_JS = {
    'core': {
        'source_filenames': (
            'js/jquery-1.9.1.min.js',
            'bootstrap/js/bootstrap.min.js',
            'js/core.js',
            'js/holder.js',
            'js/typeahead.bundle.js',
        ),
        'output_filename': 'js/core.js',
    },
    'management': {
        'source_filenames': (
            'js/jquery.hotkeys.js',
            'js/json2.js',
            'js/underscore-min.js',
            'js/backbone-min.js',
            'js/handlebars.js',
            'js/moment.min.js',
            'js/parsley.js',
            'extras/select2/select2.js',
        ),
        'output_filename': 'js/management.js',
    },
    'directory': {
        'source_filenames': (
            'extras/raty-master/lib/jquery.raty.js',
            'js/directory.js',
        ),
        'output_filename': 'js/directory.js',
    },
    'dataTables': {
        'source_filenames': (
            'extras/DataTables-1.9.4/media/js/jquery.dataTables.min.js',
        ),
        'output_filename': 'js/dataTables.js',
    }
}

CRISPY_TEMPLATE_PACK='bootstrap3'
REST_FRAMEWORK = {
    'DEFAULT_MODEL_SERIALIZER_CLASS': 
        'rest_framework.serializers.HyperlinkedModelSerializer',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_RENDERER_CLASSES': (
        # 'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
        #'rest_framework_csv.renderers.CSVRenderer',
    ),
    'PAGINATE_BY': 20
}
SWAGGER_SETTINGS = {
    "exclude_namespaces": ['management'], # List URL namespaces to ignore
    "api_version": '0.1',  # Specify your API's version
    "api_path": "/",  # Specify the path to your API not a root level
    "enabled_methods": [  # Specify which methods to enable in Swagger UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "api_key": '', # An API key
    "is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": False,  # Set to True to enforce admin only access
}
SEARCH_HOST=os.environ.get('SEARCH_HOST', '127.0.0.1')
SEARCH_PORT=os.environ.get('SEARCH_PORT', '8983')
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://%s:%s/solr' % (SEARCH_HOST, SEARCH_PORT),
        'INCLUDE_SPELLING': True
    },
}
