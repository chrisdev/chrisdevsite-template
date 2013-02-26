
from local import *

########## TEST SETTINGS
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = DJANGO_ROOT
TEST_DISCOVER_ROOT = DJANGO_ROOT
TEST_DISCOVER_PATTERN = "*"

########## IN-MEMORY TEST DATABASE

# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'memory',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

