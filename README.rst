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

    pip install -r requirements/local.txt



Running Management Commands
===========================

The starter project provides for multiple settings and requirement files. Because of this, we
generally no longer use `manage.py` to run commands such as `runserver`, `syncdb` etc.
For example we can start the development server as follows ::

    django-admin.py runserver  --settings=[myproject].settings.local

The `local.py` module is designed for local development

This turns on the DEBUG  settings, set the default database to sqlite3 (default.db)
adds `debug_toolbar` to INSTALLED_APPS and adds the debug-toolbar middleware.

For a more custom local environment you should create a new "dev" settings
module. As an example, the template project provides `dev_chris.py` which
provides for postgresql default database. To run the development server using these settings::

    django-admin.py runserver  --settings=[myproject].settings.dev_chris


To cut down the amount of typing you can store your `--settings` in an environmental
variable called DJANGO_SETTINGS_MODULE ::

    export DJANGO_SETTINGS_MODULE=[myproject].settings.dev_chris
    django-admin.py runserver

Deployment, Settings and Secrets
==================================
You need to create a YAML file called `_default.cfg` in the project_root which contains information about
your servers, prroduction or test server settings and seceret keys.  The file should never bee added to
you source control repo and should be kept in a safe place. Here is the set up of a typical  
`_default.cfg`  ::

    ---
    nginx_root:  /etc/nginx/sites-available
    test_hosts:   ['svr1.chrisdev.com']
    prod_hosts:   ['srv2.chrisdev.com']
    sites:   /usr/local/sites
    virtualenvs:   /home/django/virtualenvs/
    nginx_root:   /etc/nginx//sites-available
    gunicorn:  127.0.0.1:2013
    user:   django_user
    memcache: 127.0.0.1:11211
    db_user: db_user
    db_passwd: XXXXX
    db_host: db_host
    db_name_production: prod_site_db
    db_name_test: test_site_db
    email_from: webmaster@client.com
    email_user: info@chrisdev.com
    email_password: XXX
    email_host: mymail.com
    secret_key: django_seceret_key
    testing_site_name: test_site.chrisdev.com
    production_site_name: client.com
    akismet_api_key: XXXXX


Requirements
=============
The new project template also utilises multiple requirements files::

     _base.txt
     local.txt
     production.txt
     test.txt

`_base.txt` contains the core requirements for the project while `local.txt`
will install the django-debug-toolbar etc.::

    pip install -r requirements/local.txt



