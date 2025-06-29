from .base import *
from .base import env
from urllib.parse import urlparse
import os

DATABASES = {'default': env.db()}

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["rabbleapp.me"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=["https://rabbleapp.me"])
SECURE_SSL_REDIRECT = True

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
STATICFILES_DIRS = [BASE_DIR / "static"]

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
