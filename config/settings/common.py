from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(".env")
BASE_DIR = Path(__file__).resolve().parent.parent.parent


AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'book_list'

STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles'))

STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    "debug_toolbar",
    "django_htmx",
    "storages",

    'accounts',
    'books',
]


MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
]

INTERNAL_IPS = [ '127.0.0.1',]

ROOT_URLCONF = 'config.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
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

WSGI_APPLICATION = 'config.wsgi.application'

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Add Qdrant config
QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")

REDIS_URL = os.getenv("REDIS_URL","redis://redis:6379/0")

CELERY_BROKER_URL = REDIS_URL

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler'
#         },
#         'file': {
#             'class': 'logging.FileHandler',
#             'filename': 'general.log',
#             'formatter': 'verbose'
#         }
#     },
#     'loggers': {
#         '': {
#             'handlers': ['console', 'file'],
#             "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
#         }
#     },
#     'formatters': {
#         'verbose': {
#             'format': '{asctime} ({levelname}) - {name} - {message}',
#             'style': '{'
#         }
#     }
# }


