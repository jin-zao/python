"""
Django settings for webapp project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import logging
import sys

import bcrypt
from celery.schedules import crontab
import raven
import dj_database_url

LOG = logging.getLogger(__name__)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(APP_DIR)
SRC_DIR = os.path.dirname(BASE_DIR)
PROJECT_DIR = os.path.dirname(SRC_DIR)
WEBPACK_STAT_DIR = os.path.join(SRC_DIR, 'client')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'db')
PWA_SERVICE_WORKER_PATH = os.path.join(APP_DIR, 'static/js', 'serviceworker.js')
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis://redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_URL = os.environ.get('REDIS_URL', '{}:{}'.format(REDIS_HOST, REDIS_PORT))
SSR_URL = os.environ.get('SSR_URL', 'http://192.168.0.10:5000')
SERVER_URL = os.environ.get('SERVER_URL', 'http://192.168.0.10:8000')

SKIP_PRERENDER = False

TIMEZONE = 'Europe/London'
INTERNAL_IPS = (
    '127.0.0.1',
    'localhost'
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', bcrypt.gensalt())

# SECURITY WARNING: don't run with debug turned on in production!
ENV = os.environ.get('ENV')
DEBUG = ENV == 'develop'
PROD = ENV == 'prod'
DEBUG_404 = DEBUG
TESTING = "pytest" in sys.modules


def show_toolbar(request):
    return DEBUG


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}


ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'noelwilson2018.herokuapp.com',
    'noel-wilson-2018.herokuapp.com',
    'www.noel-wilson.co.uk',
    'www.jwnwilson.com',
    'noel-wilson.co.uk',
    'jwnwilson.com',
    os.environ.get('LOAD_BALANCER_IP', '*'),
]


# Application definition
INSTALLED_APPS = [
    'raven.contrib.django.raven_compat',
    'rest_framework',
    'wagtail.api.v2',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'modelcluster',
    'taggit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django_celery_beat',
    'polymorphic',
    'webpack_loader',
    'webapp.cms',
    'storages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'webapp.cms.middleware.PreRenderMiddleware',
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'webapp.cms.middleware.SEOMiddleware',
]

ROOT_URLCONF = 'webapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'webapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if os.environ.get('ON_HEROKU'):
    SECURE_SSL_REDIRECT = True
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
    }
elif TESTING:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    }
elif PROD:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'noelwilson2018',
            'USER': os.environ.get('POSTGRES_USER_PROD', 'docker'),
            'PASSWORD': os.environ.get('POSTGRES_PASS_PROD', 'docker'),
            'HOST': os.environ.get('POSTGRES_HOST_PROD', POSTGRES_HOST),  # set in docker-compose.yml
            'PORT': 5432  # default postgres port
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'noelwilson2018',
            'USER': os.environ.get('POSTGRES_USER', 'docker'),
            'PASSWORD': os.environ.get('POSTGRES_PASS', 'docker'),
            'HOST': POSTGRES_HOST,  # set in docker-compose.yml
            'PORT': 5432  # default postgres port
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

APPEND_SLASH = True
WAGTAIL_APPEND_SLASH = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [
    os.path.join(APP_DIR, 'static'),
    os.path.join(SRC_DIR, 'client', 'build', 'static'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

WAGTAIL_SITE_NAME = 'Noel Wilson'

if DEBUG:
    WEBPACK_LOADER = {
        'DEFAULT': {
            'BUNDLE_DIR_NAME': 'js/',
            'STATS_FILE': os.path.join(WEBPACK_STAT_DIR, 'webpack-stats.dev.json'),
            'CACHE': False
        }
    }
else:
    WEBPACK_LOADER = {
        'DEFAULT': {
            'BUNDLE_DIR_NAME': 'js/',
            'STATS_FILE': os.path.join(WEBPACK_STAT_DIR, 'webpack-stats.prod.json'),
            'CACHE': True
        }
    }
    
# Setup throwaway email address to send emails
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'jwnwilsonemail@gmail.com'
EMAIL_HOST_PASSWORD = 'Jwnwilson1'


# Setup caching
def get_cache():
    """
    Heroku specific caching settings
    """
    try:
        if TESTING:
            return {
                'default': {
                    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                    'LOCATION': 'noelwilson2018'
                }
            }
        else: 
            return {
                "default": {
                    "BACKEND": "django_redis.cache.RedisCache",
                    "LOCATION": REDIS_URL,
                    "OPTIONS": {
                        "CLIENT_CLASS": "django_redis.client.DefaultClient"
                    },
                    "KEY_PREFIX": "noelwilson2018"
                }
            }
    except Exception as e:
        LOG.error('Error loading cache falling back to memory cache: %s', str(e))
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
            }
        }


CACHES = get_cache()

# AWS stuff and sentry stuff
if PROD:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = 'noel-wilson.co.uk'
    AWS_ACCESS_KEY_ID = os.environ.get('ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.environ.get('SECRET')
    AWS_QUERYSTRING_AUTH = False

    RAVEN_CONFIG = {
        'dsn': 'https://4455bc30a01746f6ad07e8bb17fdcb7e:244d3d07cc2641b09cfede93ef8dad8e@sentry.io/646552',
        # If you are using git, you can also automatically configure the
        # release based on the git info.
        'release': os.environ['SOURCE_VERSION'] if os.environ.get('ON_HEROKU') else raven.fetch_git_sha(PROJECT_DIR)
    }

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'fixtures')
]

if TESTING:
    DEBUG = False

# Celery stuff
CELERY_BROKER_URL = REDIS_URL
BROKER_URL = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIMEZONE
CELERY_BEAT_SCHEDULE = {}
# CELERY_BEAT_SCHEDULE = {
#     'render-cache': {
#         'task': 'webapp.cms.tasks.render_cache_pages', 
#         'schedule': crontab(hour=1),
#     }          
# }

# CACHE_MIDDLEWARE_SECONDS = 60 * 60 * 60

# Don't timeout
CACHE_MIDDLEWARE_SECONDS = None

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}

if DEBUG:
    # make all loggers use the console.
    for logger in LOGGING['loggers']:
        LOGGING['loggers'][logger]['handlers'] = ['console']
