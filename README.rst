=======================
Chrisdev Site template
=======================

A Django starter project to be used for ChrisDev sites

Install Setup Virtualenv
========================

First, make sure you are using virtualenv/virtualenvwrapper::

    $ mkvirtualenv --distribute myproject-env

You will also need to ensure that the virtualenv has the project directory
added to the path. Adding the project directory will allow `django-admin.py` to be able to change settings using the `--settings` flag.

Use `add2virtualenv` which will take care of adding the project path to the `site-directory` for you::

    $ add2virtualenv /path/to/myproject

Create the Project
===================

To create the project::

    django-admin.py startproject [myproject] --template=https://github.com/chrisdev/chrisdevsite-template/zipball/master

Then install the requirements::

    pip install -r requirements/local.py



Running Management Commands
===========================

The starter project provides for multiple settings and requirement files. Because of this, we
generally no longer use `manage.py` to run commands such as `runserver`, `syncdb` etc.
For example we can start the development server as follows ::

    django-admin.py runserver  --settings=civ_monitor.settings.local

The `local` module is designed for local development::

    """Development settings and globals."""


    from os.path import join, normpath

    from base import *


    ########## DEBUG CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
    TEMPLATE_DEBUG = DEBUG
    ########## END DEBUG CONFIGURATION


    ########## EMAIL CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    ########## END EMAIL CONFIGURATION


    ########## DATABASE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': normpath(join(DJANGO_ROOT, 'default.db')),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }
    ########## END DATABASE CONFIGURATION

    ########## CACHE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }
    ########## END CACHE CONFIGURATION

    ########## TOOLBAR CONFIGURATION
    # See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
    INSTALLED_APPS += (
        'debug_toolbar',
    )

    # See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
    INTERNAL_IPS = ('127.0.0.1',)

    # See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    ########## END TOOLBAR CONFIGURATION

    import warnings
    warnings.simplefilter('error', DeprecationWarning)


This turns on the DEBUG  settings, set the default datbase to sqlite3 (default.db)
adds `debug_toolbar` to INSTALLED_APPS anad adds the debug-toolbar middleware.

For a more custom local environment you should create a new "dev" settings
module. As an example, the template project provides `dev_chris.py` which
provides for postgresql default database. To run the development server using these settings::

    django-admin.py runserver  --settings=civ_monitor.settings.dev_chris


To cut down the amount of typing you can store your `--settings` in an environmental
variable called DJANGO_SETTINGS_MODULE ::

    export DJANGO_SETTINGS_MODULE=civ_monitor.settings.dev_chris
    django-admin.py runserver



Requirements
=============
The new project template also utilizes multiple requirements files::

     _base.txt
     local.txt
     production.txt
     test.txt

`_base.txt` contains the core requirements for the project while `local.txt`
will install the django-debug-toolbar etc.::

    pip install -r requirements/local.py










