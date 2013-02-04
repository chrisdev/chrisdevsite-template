=======================
Chrisdev Site template
=======================

A Django starter project to be used for ChrisDev sites

Installation of Dependencies
============================

First, make sure you are using virtualenv/virtualenvwrapper::

    $ mkvirtualenv --distribute myproject-env

You will also need to ensure that the virtualenv has the project directory
added to the path. Adding the project directory will allow `django-admin.py` to be able to change settings using the `--settings` flag.

Use `add2virtualenv` which will take care of adding the project path to the `site-directory` for you::

    $ add2virtualenv /path/to/myproject


To create the project::

    $ django-admin.py startproject [myproject] --template=https://github.com/chrisdev/chrisdevsite-template/zipball/master





