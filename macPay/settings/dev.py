from .base import *

DEBUG = True

TEMPLATE_DEBUG = True

THIRD_PARTY_APPS = (
    'debug_toolbar',
    'autofixture',
)

INSTALLED_APPS += THIRD_PARTY_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_ROOT = 'staticfiles'