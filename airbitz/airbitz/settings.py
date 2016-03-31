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

# Celery
import djcelery
djcelery.setup_loader()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
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

# SEO RELATED
CANONICAL_BASE = 'https://airbitz.co'

SCREENCAP_ABSOLUTE_URL = 'https://airbitz.co'
SCREENCAP_INTERVAL = datetime.timedelta(minutes=15)


# FRONT PAGE QUERY RELATED
FP_QUERY_INTERVAL = datetime.timedelta(days=7)

DEPLOY_DATE = '20140507'

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

    'djcelery',
    'djrill',
    'mailchimp',
    'haystack',
    'celery_haystack',
    'imagekit',
    'pipeline',
    'crispy_forms',
    'bootstrap_pagination',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_throttling',
    'south',
    'rest_framework_swagger',
    'analytical',
    'absolute',
    'clear_cache',

    'restapi',
    'affiliates',
    'location',
    'directory',
    'management',
    'notifications',
    'statistics',
    'verification',
)
if DEBUG:
    INSTALLED_APPS += (
        'django_extensions',
    )

if DEBUG:
    IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'imagekit.cachefiles.strategies.Optimistic'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'airbitz.middleware.SessionExpiry',
    'airbitz.middleware.SetRemoteAddr',
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
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
    'airbitz.processors.get_canonical',
    'absolute.context_processors.absolute'
)

ROOT_URLCONF = 'airbitz.urls'

WSGI_APPLICATION = 'airbitz.wsgi.application'

if not DEBUG:
    ALLOWED_HOSTS = [
            'admin.airbitz.co',
            'test-directory.airbitz.co',
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

PIPELINE_JS = {
    'core': {
        'source_filenames': (
            'js/jquery-1.11.0.min.js',
            'bootstrap/js/bootstrap.min.js',
            'extras/jquery-cookie-master/src/jquery.cookie.js',
            'js/modernizr.js',
            'js/bowser.js',
            'js/enquire.js',
            'js/core.js',
            'js/holder.js',
            'js/typeahead.bundle.js',
            'extras/retinajs-master/retina.js',
            'extras/jQuery.dotdotdot-master/src/js/jquery.dotdotdot.min.js',
            'extras/Readmore.js-master/readmore.min.js',
            'extras/swipebox-master/source/jquery.swipebox.min.js',
            'extras/bootstrap-hover-dropdown-master/bootstrap-hover-dropdown.js',
            'js/frontend-ui.js',
            'js/mobile-download-bar.js'
        ),
        'output_filename': 'js/core.' + DEPLOY_DATE + '.js',
    },
    'home': {
        'source_filenames': (
            'extras/backstretch/backstretch.js',
            'extras/ajaxchimp/jquery.ajaxchimp.js',
            'extras/carouFredSel-6.2.1/jquery.carouFredSel-6.2.1-packed.js',
            'extras/Magnific-Popup-master/dist/jquery.magnific-popup.js',
            'extras/particlesjs/particles.js',
            'js/home-ui.js',
        ),
        'output_filename': 'js/home.' + DEPLOY_DATE + '.js',
    },
    'airbitz-theme-head': {
        'source_filenames': (
            'airbitz-theme/vendor/modernizr/modernizr.js',
        ),
        'output_filename': 'js/airbitz-theme-head.' + DEPLOY_DATE + '.js',
    },
    'airbitz-theme-head-ie-8': {
        'source_filenames': (
            'airbitz-theme/vendor/respond/respond.js',
            'airbitz-theme/vendor/excanvas/excanvas.js',
        ),
        'output_filename': 'js/airbitz-theme-head-ie-8.' + DEPLOY_DATE + '.js',
    },
    'airbitz-theme-footer-jquery-gt-ie-9': {
        'source_filenames': (
            'airbitz-theme/vendor/jquery/jquery.js',
        ),
        'output_filename': 'js/airbitz-theme-footer-jquery-gt-ie-9.' + DEPLOY_DATE + '.js',
    },
    'airbitz-theme-footer': {
        'source_filenames': (
            'airbitz-theme/vendor/jquery.appear/jquery.appear.js',
            'airbitz-theme/vendor/jquery.easing/jquery.easing.js',
            'airbitz-theme/vendor/jquery-cookie/jquery-cookie.js',
            'airbitz-theme/vendor/bootstrap/bootstrap.js',
            'airbitz-theme/vendor/common/common.js',
            'airbitz-theme/vendor/jquery.validation/jquery.validation.js',
            'airbitz-theme/vendor/jquery.stellar/jquery.stellar.js',
            'airbitz-theme/vendor/owlcarousel/owl.carousel.js',

            'airbitz-theme/js/theme.js',

            'airbitz-theme/vendor/rs-plugin/js/jquery.themepunch.tools.min.js',
            'airbitz-theme/vendor/rs-plugin/js/jquery.themepunch.revolution.min.js',
            'airbitz-theme/vendor/circle-flip-slideshow/js/jquery.flipshow.js',

            'extras/ajaxchimp/jquery.ajaxchimp.js',

            'airbitz-theme/js/custom.js',
            'airbitz-theme/js/theme.init.js',
        ),
        'output_filename': 'js/airbitz-theme.' + DEPLOY_DATE + '.js',
    },
    'page_content': {
        'source_filenames': (
            'extras/backstretch/backstretch.js',
            'extras/carouFredSel-6.2.1/jquery.carouFredSel-6.2.1-packed.js',
            'extras/Magnific-Popup-master/dist/jquery.magnific-popup.js',
            'extras/FitVids.js-master/jquery.fitvids.js',
            'extras/highlightjs/highlight.js',
            'js/page_content.js',
        ),
        'output_filename': 'js/page-content.' + DEPLOY_DATE + '.js',
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
            'extras/masonry/masonry.pkgd.min.js',
            'extras/blur.js/blur.js',
            'extras/ajaxchimp/jquery.ajaxchimp.js',
            'js/directory.js',
        ),
        'output_filename': 'js/search.' + DEPLOY_DATE + '.js',
    },
    'search_starter': {
        'source_filenames': (
            'searchStarter/app.js',
            'searchStarter/controllers/.js',
        ),
        'output_filename': 'js/search-starter.min.js',
    },
    'business_add': {
        'source_filenames': (
            'extras/blur.js/blur.js',
            'extras/select2/select2.js',
            'js/moment.min.js',
            'extras/jquery.imgareaselect-0.9.10/scripts/jquery.imgareaselect.min.js',
            'extras/bootstrap-datetimepicker-master/build/js/bootstrap-datetimepicker.min.js',
            'angular/ngAutocomplete.js',
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
PIPELINE_CSS = {
    'global': {
        'source_filenames': (
            'bootstrap/css/bootstrap.css',
            'extras/font-awesome/css/font-awesome.min.css',
            'extras/swipebox-master/source/swipebox.css',
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
            'extras/Magnific-Popup-master/dist/magnific-popup.css',
            'css/home.css',
        ),
        'output_filename': 'css/home.' + DEPLOY_DATE + '.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'page_content': {
        'source_filenames': (
            'css/animate.css',
            'extras/Magnific-Popup-master/dist/magnific-popup.css',
            'extras/highlightjs/highlight.css',
            'css/page-content.css',
        ),
        'output_filename': 'css/page-conent.' + DEPLOY_DATE + '.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'app_download': {
        'source_filenames': (
            'css/animate.css',
            'css/app-download.css',
        ),
        'output_filename': 'css/app-download.' + DEPLOY_DATE + '.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'search': {
        'source_filenames': (
            'css/animate.css',
            'css/results-map-list.css',
            'css/results-grid.css',
        ),
        'output_filename': 'css/search.' + DEPLOY_DATE + '.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'search_no_results': {
        'source_filenames': (
            'css/animate.css',
            'css/search-no-results.css',
        ),
        'output_filename': 'css/search-no-results.' + DEPLOY_DATE + '.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    'search_starter': {
        'source_filenames': (
            'css/ng-searchStarter.css',
        ),
        'output_filename': 'css/ng-searchStarter.' + DEPLOY_DATE + '.css',
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
    'DEFAULT_THROTTLE_RATES': {
        'per_user_throttle': '100/sec',
        'anon': '100/sec',
    },
    'PAGINATE_BY': 20
}
REST_FRAMEWORK_THROTTLING = {
    'DEFAULT_NEW_USER_THROTTLE': True,
    'DEFAULT_NEW_USER_THROTTLE_RATE': '1000000/min',
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

HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'
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
        'api_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/tmp/api.log',
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
       'restapi': {
            'handlers': ['api_file'],
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
    API_GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-11111111-11'
    API_PIWIK_TOKEN = 'e96aaf8ea583645a2b7f6290c536c984'
    API_PIWIK_SITE_ID = 1000
    API_PIWIK_STATS_SITE_ID = 1000
else:
    GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-47697034-1'
    API_GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-47697034-3'
    API_PIWIK_TOKEN = 'e96aaf8ea583645a2b7f6290c536c984'
    API_PIWIK_SITE_ID = 2
    API_PIWIK_STATS_SITE_ID = 8

if DEBUG:
    DEVELOPER_BITID_HOST = 'http://10.10.8.155:8000/bitid-login/'
else:
    DEVELOPER_BITID_HOST = 'https://developer.airbitz.co/bitid-login/'

# MANDRILL TRANSACTIONAL EMAIL SETTINGS
EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'
MANDRILL_API_KEY = "PyTes5t81HtIAenr0KNtxw"


# MAILCHIMP API KEYS
MAILCHIMP_API_KEY = "8e5665e638ab8540f17772fbfa96d15e-us3"
MAILCHIMP_LIST_AIRBITZ_MAIN = "b7bd36890d"
