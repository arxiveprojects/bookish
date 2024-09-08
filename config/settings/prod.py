from .common import *


DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY','django-insecure-6j2@8g)ygvsiuvnh1w8cs&o)k**r')
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS','*')]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
    }
}


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID','AKIAUGYIA5HL2TEBDKMI')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY','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')
AWS_STORAGE_BUCKET_NAME = 'bookishpdf'
AWS_S3_REGION_NAME = 'ap-south-1'


# Static files (CSS, JavaScript, Images)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/'

# Media files (Uploaded PDFs, etc.)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'

# Configure S3 settings
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

# SECURE_SSL_REDIRECT = os.environ.get("DJANGO_SECURE_SSL_REDIRECT", True)
# SECURE_HSTS_SECONDS = os.environ.get("DJANGO_SECURE_HSTS_SECONDS",2592000)
# SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", True)
# SECURE_HSTS_PRELOAD = os.environ.get("DJANGO_SECURE_HSTS_PRELOAD", True)
# SESSION_COOKIE_SECURE = os.environ.get("DJANGO_SESSION_COOKIE_SECURE", True)
# CSRF_COOKIE_SECURE = os.environ.get("DJANGO_CSRF_COOKIE_SECURE", True)
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') 

# CACHE_MIDDLEWARE_ALIAS = 'default'
# CACHE_MIDDLEWARE_SECONDS = 604800
# CACHE_MIDDLEWARE_KEY_PREFIX = ''
