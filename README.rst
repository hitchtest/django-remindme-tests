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

    $ brew install python python3 redis postgresql git libtool automake npm

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

Then, on Linux, run::

  $ hitch test simple_reminder.test

On Mac OS X, run::

  $ hitch test simple_reminder.test --settings macos.yml

You may need to tweak some of the version settings in macos.yml or
settings.yml to get it to run, if your version of postgres or redis
are slightly different to the ones specified.

This should demonstrate one test *passing* (with python 2.7) and one test
failing (with python 3.4).

Caveats
=======

* The tests will only run on *nix systems. Windows is not supported.
* Sometimes the latest version of firefox does not work correctly with selenium. If you are experiencing selenium errors, try downgrading firefox one or two versions.


.. _Django-RemindMe: https://github.com/hitchtest/django-remindme
.. _pipsi: https://github.com/mitsuhiko/pipsi
