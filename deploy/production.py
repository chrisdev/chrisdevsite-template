#For use with the fabric deploy_settings and appropriate YAML
from .base import *

DATABASES = {
   "default": {
       "ENGINE": "django.db.backends.postgresql_psycopg2",
       "NAME": "%(db_name)s",
       "USER": "%(db_user)s",
      "PASSWORD": "%(db_passwd)s",
     "HOST": "%(db_host)s",
   }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '%(memcache)s',
    }
}

CACHE_MIDDLEWARE_SECONDS=60*5
CACHE_MIDDLEWARE_KEY_PREFIX = "national-hiv-site"



ADMINS = [
     ("Chris Clarke", "cclarke@chrisdev.com"),
]

MANAGERS = [
     ("Chris Clarke", "cclarke@chrisdev.com"),

]


CONTACT_EMAIL='%(email_from)s'

AKISMET_API_KEY='b6c89762bc6a'

DEFAULT_FROM_EMAIL= '%(email_from)s'
EMAIL_USE_TLS = True
EMAIL_HOST = '%(email_host)s'
EMAIL_HOST_USER = '%(email_user)s'
EMAIL_HOST_PASSWORD = '%(email_password)s'
EMAIL_PORT = 587
