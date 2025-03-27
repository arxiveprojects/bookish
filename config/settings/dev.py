from .common import *

DEBUG = True
SECRET_KEY = "django-insecure-6j2@8g)ygvsiuvnh1w8cs&o)k**r"

ALLOWED_HOSTS = ["*"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.{}'.format(
             os.getenv('DATABASE_ENGINE', 'sqlite3')
         ),
        "NAME": os.getenv("DB_NAME", BASE_DIR / "db.sqlite3"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}
os.getenv

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

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