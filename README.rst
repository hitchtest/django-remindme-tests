Django-RemindMe-Test
====================

Django-RemindMe-Test is an example test + engine using hitch for use with the
example Django-RemindMe_ application.

To emphasize the isolation from the application itself, it's in a different
repository.

It's very easy to set up...

Set up
======

You must have Postgresql, Redis, Python and Virtualenv installed before continuing.

On Ubuntu::

    $ sudo apt-get install python python-virtualenv python-pip postgresql redis-server git firefox node-less automake libtool

    $ sudo pip install hitch

On Mac OS X::

    $ brew install python python3 redis postgresql git libtool automake npm

    $ npm install -g less

    $ pip install -U setuptools pip virtualenv hitch


First clone the django-remindme project::

  $ git clone https://github.com/hitchtest/django-remindme.git

Then enter the Django-Remindme directory and clone this project inside it::

  $ git clone https://github.com/hitchtest/django-remindme-tests.git

Run
===

Enter the django-remindme/django-remindme-tests/ folder and run::

  $ hitch init

Then run::

  $ hitch test simple_reminder.test

You may need to tweak some of the version settings in settings.yml
to accomodate the different version of postgresql or redis you are
running.

This should demonstrate one test *passing* (with python 2.7) and one test
*failing* (with python 3.4). The fix to make django-remindme work
in python 3 is very simple.

Caveats
=======

* The tests will only run on *nix systems. Windows is not supported.
* Sometimes the latest version of firefox does not work correctly with selenium. If you are experiencing selenium/firefox errors, try downgrading firefox one or two versions.


.. _Django-RemindMe: https://github.com/hitchtest/django-remindme
.. _pipsi: https://github.com/mitsuhiko/pipsi
