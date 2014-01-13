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
    'imagekit',
    'pipeline',
    'crispy_forms',
    'rest_framework',
    'south',

    'restapi',
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
    MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
else:
    MEDIA_ROOT = os.path.join(os.environ['HOME'], 'media')

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static/'),
)
PIPELINE_CSS = {
    'global': {
        'source_filenames': (
            'bootstrap/css/bootstrap.css',
            'bootstrap/css/bootstrap-responsive.css',
            'css/global-stylesheet.css',
        ),
        'output_filename': 'css/global.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
}
PIPELINE_JS = {
    'core': {
        'source_filenames': (
            'js/jquery-1.9.1.min.js',
            'js/json2.js',
            'js/underscore-min.js',
            'js/backbone-min.js',
            'js/handlebars.js',
            'js/holder.js',
            'js/typeahead.js',
        ),
        'output_filename': 'js/core.js',
    },
}

CRISPY_TEMPLATE_PACK='bootstrap3'
REST_FRAMEWORK = {
    'DEFAULT_MODEL_SERIALIZER_CLASS': 
        'rest_framework.serializers.HyperlinkedModelSerializer',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
SWAGGER_SETTINGS = {
    "exclude_namespaces": [], # List URL namespaces to ignore
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
