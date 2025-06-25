from .base import *
from .base import env
from urllib.parse import urlparse

DATABASES = {'default': env.db()}

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["your-domain.com"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=["https://your-domain.com"])
SECURE_SSL_REDIRECT = True

STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MIDDLEWARE += ["whitenoise.middleware.WhiteNoiseMiddleware"]
