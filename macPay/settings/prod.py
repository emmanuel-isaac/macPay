from .base import *

# Parse database configuration from $DATABASE_URL
import dj_database_url

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

DEBUG = False

TEMPLATE_DEBUG = False

# Static asset configuration
STATIC_ROOT = 'staticfiles'

DATABASES = {
    'default': dj_database_url.config(),
}

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'