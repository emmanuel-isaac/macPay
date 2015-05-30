from base import *

DEBUG = True

TEMPLATE_DEBUG = True

STATIC_ROOT = 'staticfiles'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

THIRD_PARTY_APPS = (
    'debug_toolbar',
    'autofixture',
)

INSTALLED_APPS += THIRD_PARTY_APPS

STATIC_ROOT = 'staticfiles'