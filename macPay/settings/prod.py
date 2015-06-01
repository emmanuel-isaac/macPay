from .base import *

# Parse database configuration from $DATABASE_URL
import dj_database_url
import envvars
envvars.load()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

DEBUG = envvars.get('DEBUG')

TEMPLATE_DEBUG = False

# Static asset configuration
#STATIC_ROOT = 'staticfiles'
import os

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DATABASES = {
    'default': dj_database_url.config(),
}

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'