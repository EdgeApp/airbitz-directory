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

prod_usernames = ('bitz', 'root', )
DEBUG = os.environ.get('USER') not in prod_usernames

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vjhh1t5!3t69w%ytjq5+@u12hh)(qme(&kkxzdmf%gy*&x4cur'

if DEBUG:
    TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []
GOOGLE_MAP_KEY = 'AIzaSyBMrEE7BCy4O7DPHEdUmz0Sa8DoGQc-tXk'
GOOGLE_SERVER_KEY = 'AIzaSyDQAC7mDZWLlKD_K31y4hsiVtHSj8pmhgQ'

FS_CLIENT_ID='JYRB30J3V1EVKVTIKFOZQ1NZ4Z5CVL2WYCJUEIBABTDFIHFJ'
FS_CLIENT_SECRET='HQCHFV2B5SPZUUPTADYHYZRYNYZH0NG4LM3FUKNWFSP0UU4Y'

SESSION_EXPIRY=60 * 60

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
    'bootstrap_pagination',
    'rest_framework',
    'rest_framework.authtoken',
    'south',
    'rest_framework_swagger',
    'analytical',
    'absolute',

    'restapi',
    'location',
    'directory',
    'management',
)
if DEBUG:
    INSTALLED_APPS += (
        'django_extensions',
    )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
    'airbitz.middleware.SessionExpiry',
    'airbitz.middleware.SetRemoteAddr',
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
    'airbitz.processors.debug',
    'absolute.context_processors.absolute'
)

ROOT_URLCONF = 'airbitz.urls'

WSGI_APPLICATION = 'airbitz.wsgi.application'

if not DEBUG:
    ALLOWED_HOSTS = [
            'admin.airbitz.co',
            'api.airbitz.co',
            'demo.airbitz.co',
            'airbitz.co']

if os.environ.has_key('DATABASE_HOST'):
    DB_HOST = os.environ.get('DATABASE_HOST')
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
    MEDIA_ROOT = os.path.join('/home/bitz/', 'media')
    MEDIA_URL = '/media/'


# STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.environ['HOME'], 'static')
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static/'),
)
if not DEBUG:
    USE_X_FORWARDED_HOST=True

if True or DEBUG:
    PIPELINE_ENABLED=False
else:
    PIPELINE_ENABLED=True
    PIPELINE_AUTO = False
    PIPELINE_VERSION = True

PIPELINE_CSS = {
    'global': {
        'source_filenames': (
            'bootstrap/css/bootstrap.css',
            'extras/swipebox-master/source/swipebox.css',
            'extras/jvectormap/jquery-jvectormap.css',
            'css/global-stylesheet.css',
        ),
        'output_filename': 'css/global.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'home': {
        'source_filenames': (
            'css/animate.css',
            'css/home.css',
        ),
        'output_filename': 'css/home.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'management': {
        'source_filenames': (
            'extras/select2/select2.css',
            'css/global-management.css',
            'extras/jquery.imgareaselect-0.9.10/css/imgareaselect-default.css',
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
            'js/jquery-1.11.0.min.js',
            'bootstrap/js/bootstrap.min.js',
            'js/modernizr.js',
            'js/bowser.js',
            'js/enquire.js',
            'js/core.js',
            'js/holder.js',
            'js/typeahead.bundle.js',
            'extras/jQuery.dotdotdot-master/src/js/jquery.dotdotdot.min.js',
            'extras/Readmore.js-master/readmore.min.js',
            'extras/colorbox-master/jquery.colorbox-min.js',
            'extras/swipebox-master/source/jquery.swipebox.min.js',
            'js/frontend-ui.js'
        ),
        'output_filename': 'js/core.js',
    },
    'home': {
        'source_filenames': (
            'js/jquery-1.11.0.min.js',
            'extras/ajaxchimp/jquery.ajaxchimp.js',
            'extras/jquery.marquee/jquery.marquee.min.js',
            'js/frontend-ui.js',
            'js/home-ui.js',
        ),
        'output_filename': 'js/home.js',
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
            'extras/jquery.imgareaselect-0.9.10/scripts/jquery.imgareaselect.min.js',
        ),
        'output_filename': 'js/management.js',
    },
    'directory': {
        'source_filenames': (
            'extras/gmaps/gmaps.js',
            'extras/jvectormap/jquery-jvectormap.js',
            'extras/jvectormap/maps/jquery-jvectormap-us-aea-en.js',
            'extras/jvectormap/maps/jquery-jvectormap-ca-lcc-en.js',
            'extras/jvectormap/maps/jquery-jvectormap-europe-mill-en.js',
            'extras/masonry/masonry.pkgd.min.js',
            'extras/blur.js/blur.js',
            'extras/ajaxchimp/jquery.ajaxchimp.js',
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
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
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
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'helo@airbitz.co'
EMAIL_HOST_PASSWORD = 'abhello!1'
EMAIL_PORT = 465
ADMINS=(('Damian', 'damian@airbitz.co'), ('Tim', 'tim@airbitz.co'))
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'verbose':    {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/tmp/django-app.log',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'requests':  {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/tmp/django-request.log'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['requests'],
            'level': 'INFO',
            'propagate': True,
        },
       'airbitz': {
            'handlers': ['file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}

# GOOGLE ANALYTICS
if DEBUG:
    # bogus id unless in production to prevent analytics pollution
    GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-11111111-11'
else:
    GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-47697034-1'
