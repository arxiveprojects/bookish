from .common import *

DEBUG = True
SECRET_KEY = 'django-insecure-6j2@8g)ygvsiuvnh1w8cs&o)k**r'

ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ["127.0.0.1",]


# DATABASES = {
#  'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': 'book',
#     'USER': 'ik',
#     'PASSWORD': 'ik98',
#     'PORT': 5432
#  }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}