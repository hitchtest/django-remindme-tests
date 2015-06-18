Django-RemindMe-Test
====================

Django-RemindMe-Test is an example test + engine using hitch for use with the
example Django-RemindMe_ application.

To emphasize the isolation from the application itself, it's in a different
repository.

Setup
=====

You must have Postgresql, Redis, Python and Virtualenv installed before continuing.

On Ubuntu::

    $ sudo apt-get install python python-virtualenv python-pip postgresql redis-server git firefox node-less automake libtool

On Mac OS X::

    $ brew install python redis postgresql git libtool automake npm

    $ npm install -g less

    $ pip install -U setuptools pip virtualenv

To install hitch::

  $ sudo pip install hitch

Or, if you don't like using root, install pipsi_ first and then run::

  $ pipsi install hitch

First clone the django-remindme project::

  $ git clone https://github.com/hitchtest/django-remindme.git

Then enter the Django-Remindme directory and clone this project inside it::

  $ git clone https://github.com/hitchtest/django-remindme-tests.git

Run
===

Enter the django-remindme/django-remindme-tests/ folder and run::

  $ hitch init

Then run::

  $ hitch test .

You may need to tweak some of the settings to get it to run.

This should demonstrate one test *passing* (with python 2.7) and one test
failing (with python 3.4).

Run with different settings
===========================

You can run with a different settings file to settings.yml::

  $ hitch test simple_reminder.test --settings macos.yml

You can also amend settings directly from the command line using JSON, e.g.::

  $ hitch test simple_reminder.test --settings macos.yml --extra '{"postgres_version": "3.5.5"}'

Caveats
=======

* The tests will only run on *nix systems. Windows is not supported.


.. _Django-RemindMe: https://github.com/hitchtest/django-remindme
.. _pipsi: https://github.com/mitsuhiko/pipsi
