from .base import *
from .base import env
from urllib.parse import urlparse
import os

DATABASES = {'default': env.db()}

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["your-domain.com"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=["https://your-domain.com"])
SECURE_SSL_REDIRECT = False

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

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
