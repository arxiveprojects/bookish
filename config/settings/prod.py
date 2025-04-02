from .common import *
import dj_database_url

DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(",")

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'bookishpdf'
AWS_S3_REGION_NAME = 'us-east-1'

# Static files (CSS, JavaScript, Images)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/'

# Media files (Uploaded PDFs, etc.)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'

# S3 Configuration
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False


# DATABASES = {
#     'default': dj_database_url.config()
# }



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        }
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} ({levelname}) - {name} - {message}',
            'style': '{'
        }
    }
}

# SECURE_SSL_REDIRECT = os.getenv("DJANGO_SECURE_SSL_REDIRECT", True)
# SECURE_HSTS_SECONDS = os.getenv("DJANGO_SECURE_HSTS_SECONDS",2592000)
# SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", True)
# SECURE_HSTS_PRELOAD = os.getenv("DJANGO_SECURE_HSTS_PRELOAD", True)
# SESSION_COOKIE_SECURE = os.getenv("DJANGO_SESSION_COOKIE_SECURE", True)
# CSRF_COOKIE_SECURE = os.getenv("DJANGO_CSRF_COOKIE_SECURE", True)
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') 

# CACHE_MIDDLEWARE_ALIAS = 'default'
# CACHE_MIDDLEWARE_SECONDS = 604800 
# CACHE_MIDDLEWARE_KEY_PREFIX = ''  


