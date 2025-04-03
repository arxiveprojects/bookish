from .common import *
# import dj_database_url

DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(",")

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'


# Configure S3 settings
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False

# S3 static settings
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

STORAGES = {
    "default": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage",},
    "staticfiles": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage", },
}



# DATABASES = {
#     'default': dj_database_url.config()
# }

DATABASES = {
    "default": {
        "ENGINE": f"django.db.backends.{os.getenv('DB_ENGINE')}",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

REDIS_URL = os.getenv("REDIS_URL","redis://redis:6379/0")
CELERY_BROKER_URL = REDIS_URL
CELERY_TASK_ALWAYS_EAGER = True

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

