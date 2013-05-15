#production.py

from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = get_env_variable("SECRET_KEY")

DATABASES = {
   "default": {
       "ENGINE": "django.db.backends.postgresql_psycopg2",
       "NAME":  get_env_variable("DB_NAME"),
       "USER": get_env_variable("DB_USER"),
      "PASSWORD": get_env_variable("DB_PASSWD"),
     "HOST": get_env_variable("DB_HOST"),
   }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': get_env_variable('MEMCACHE_PORT'),
    }
}

CACHE_MIDDLEWARE_SECONDS=60*5
CACHE_MIDDLEWARE_KEY_PREFIX = "{{ project_name }}"
INSTALLED_APPS += [
    'gunicorn',
]

ALLOWED_HOSTS = [get_env_variable("SITE_NAME"),]

ADMINS = [
     ("Chris Clarke", "cclarke@chrisdev.com"),
]

MANAGERS = [
     ("Chris Clarke", "cclarke@chrisdev.com"),

]


CONTACT_EMAIL='website@foreign.gov.tt'

AKISMET_API_KEY=get_env_variable('AKISMET_API_KEY')

DEFAULT_FROM_EMAIL= 'website@foreign.gov.tt'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = get_env_variable('EMAIL_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_PASSWORD')
EMAIL_PORT = 587

