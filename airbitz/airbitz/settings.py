"""
Django settings for airbitz project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import getpass
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_HOST = 'localhost'

local_usernames = ('vagrant', )
staging_usernames = ('devbitz', )
prod_usernames = ('bitz', 'root', )

SYS_USER = getpass.getuser()

LOCAL = SYS_USER in local_usernames
STAGING = SYS_USER in staging_usernames
PRODUCTION = SYS_USER in prod_usernames

DEBUG = not PRODUCTION # EVERYTHING BUT PRODUCTION IS DEBUG
TEMPLATE_DEBUG = DEBUG

if DEBUG:
    print 'DEBUG:', DEBUG
    print 'LOCAL:', LOCAL
    print 'STAGING:', STAGING
    print 'PRODUCTION:', PRODUCTION

SCREENCAP_ABSOLUTE_URL = 'https://airbitz.co'
SCREENCAP_INTERVAL = datetime.timedelta(minutes=15)

DEPLOY_DATE = '20140502'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vjhh1t5!3t69w%ytjq5+@u12hh)(qme(&kkxzdmf%gy*&x4cur'

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
    'clear_cache',

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
    'airbitz.processors.active_regions',
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
CACHES = {
    "default": {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": "127.0.0.1:6379:1",
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
if LOCAL:
    MEDIA_ROOT = '/staging/media'
    MEDIA_URL = '/media/'
else:
    MEDIA_ROOT = os.path.join(os.environ['HOME'], 'media')
    MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.environ['HOME'], 'static')
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static/'),
)
if not DEBUG:
    USE_X_FORWARDED_HOST = True

if LOCAL:
    PIPELINE_ENABLED = False
else:
    STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
    PIPELINE_ENABLED = True
    PIPELINE_DISABLE_WRAPPER = True
    PIPELINE_VERSION = False # currently using DEPLOY_DATE to manually accomplish this feature
    PIPELINE_JS_COMPRESSOR = False # yuglify does not include all files (seems to leave out things that fail linting)

PIPELINE_CSS = {
    'global': {
        'source_filenames': (
            'bootstrap/css/bootstrap.css',
            'extras/font-awesome/css/font-awesome.min.css',
            'extras/swipebox-master/source/swipebox.css',
            'extras/jvectormap/jquery-jvectormap.css',
            'css/global-stylesheet.css',
        ),
        'output_filename': 'css/global.' + DEPLOY_DATE + '.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'home': {
        'source_filenames': (
            'css/animate.css',
            'css/home.css',
        ),
        'output_filename': 'css/home.' + DEPLOY_DATE + '.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'search': {
        'source_filenames': (
            'css/animate.css',
            'css/search-results.css',
        ),
        'output_filename': 'css/search.' + DEPLOY_DATE + '.css',
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
        'output_filename': 'css/management.' + DEPLOY_DATE + '.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'business_add': {
        'source_filenames': (
            'css/animate.css',
            'extras/select2/select2.css',
            'extras/jquery.imgareaselect-0.9.10/css/imgareaselect-default.css',
            'extras/bootstrap-datetimepicker-master/build/css/bootstrap-datetimepicker.css',
            'css/business-add.css',
        ),
        'output_filename': 'css/business-add.min.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'dataTables': {
        'source_filenames': (
            # 'extras/DataTables-1.9.4/media/css/jquery.dataTables.css',
            'extras/DataTables-1.10.0/media/css/jquery.dataTables.css',
        ),
        'output_filename': 'css/dataTables.' + DEPLOY_DATE + '.css',
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
        'output_filename': 'js/core.' + DEPLOY_DATE + '.js',
    },
    'home': {
        'source_filenames': (
            'extras/jvectormap/jquery-jvectormap.js',
            'extras/jvectormap/maps/jquery-jvectormap-us-aea-en.js',
            'extras/jvectormap/maps/jquery-jvectormap-ca-lcc-en.js',
            'extras/jvectormap/maps/jquery-jvectormap-europe-mill-en.js',
            'extras/ajaxchimp/jquery.ajaxchimp.js',
            'js/region-map.js',
            'js/home-ui.js',
        ),
        'output_filename': 'js/home.' + DEPLOY_DATE + '.js',
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
            'js/mgmt-ui.js',
        ),
        'output_filename': 'js/management.' + DEPLOY_DATE + '.js',
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
        'output_filename': 'js/directory.' + DEPLOY_DATE + '.js',
    },
    'search': {
        'source_filenames': (
            'extras/gmaps/gmaps.js',
            'extras/jvectormap/jquery-jvectormap.js',
            'extras/jvectormap/maps/jquery-jvectormap-us-aea-en.js',
            'extras/jvectormap/maps/jquery-jvectormap-ca-lcc-en.js',
            'extras/jvectormap/maps/jquery-jvectormap-europe-mill-en.js',
            'extras/masonry/masonry.pkgd.min.js',
            'extras/blur.js/blur.js',
            'extras/ajaxchimp/jquery.ajaxchimp.js',
            'js/region-map.js',
            'js/directory.js',
        ),
        'output_filename': 'js/search.' + DEPLOY_DATE + '.js',
    },
    'business_add': {
        'source_filenames': (
            'extras/blur.js/blur.js',
            'extras/select2/select2.js',
            'extras/backstretch/backstretch.js',
            'js/moment.min.js',
            'extras/jquery.imgareaselect-0.9.10/scripts/jquery.imgareaselect.min.js',
            'extras/bootstrap-datetimepicker-master/build/js/bootstrap-datetimepicker.min.js',
            'businessAdd/app.js',
            'businessAdd/controllers/addBizCtrl.js',
            'businessAdd/controllers/collectAllInfo.js',
            'businessAdd/controllers/generalInfoCtrl.js',
            'businessAdd/controllers/locationInfoCtrl.js',
            'businessAdd/controllers/geoInfoCtrl.js',
            'businessAdd/controllers/socialInfoCtrl.js',
            'businessAdd/controllers/bizHoursCtrl.js',
            'businessAdd/controllers/bizQueryCtrl.js',
            'businessAdd/services/abDataFactory.js',
            'businessAdd/directives/ngAutocomplete.js',
            'businessAdd/filters/miscFilters.js',
            'js/business-add.js',
        ),
        'output_filename': 'js/business-add.min.js',
    },
    'angularjs': {
        'source_filenames': (
            # 'angular/angular-1.3.0-beta.11.min.js',
            # 'angular/angular-1.2.17.js',
            'angular/angular.js',
            'angular/angular-ui-router.js',
            'angular/angular-animate.js',
            'angular/ui-bootstrap-tpls-0.11.0.js'
        ),
        'output_filename': 'js/angular.js',
    },
    'dataTables': {
        'source_filenames': (
            # 'extras/DataTables-1.9.4/media/js/jquery.dataTables.min.js',
            'extras/DataTables-1.10.0/media/js/jquery.dataTables.min.js',
            'extras/dataTables.fixedHeader/dataTables.fixedHeader.min.js',
        ),
        'output_filename': 'js/dataTables.' + DEPLOY_DATE + '.js',
    },
    'googlePlaceAutocomplete': {
        'source_filenames': (
            'extras/Google/placeAutocomplete.js',
        ),
        'output_filename': 'js/googlePlaceAutocomplete.' + DEPLOY_DATE + '.js',
    },
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
            'level': 'DEBUG',
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
            'level': 'DEBUG',
            'propagate': True,
        },
       'airbitz': {
            'handlers': ['file', 'mail_admins'],
            'level': 'DEBUG',
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
