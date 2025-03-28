from .common import *

DEBUG = True
SECRET_KEY = "django-insecure-6j2@8g)ygvsiuvnh1w8cs&o)k**r"

ALLOWED_HOSTS = ["*"]


# DATABASES = {
#     "default": {
#         "ENGINE": 'django.db.backends.{}'.format( os.getenv('DB_ENGINE', 'sqlite3') ),
#         "NAME": os.getenv("DB_NAME", BASE_DIR / "db.sqlite3"),
#         "USER": os.getenv("DB_USER"),
#         "PASSWORD": os.getenv("DB_PASSWORD"),
#         "HOST": os.getenv("DB_HOST"),
#         "PORT": os.getenv("DB_PORT"),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

