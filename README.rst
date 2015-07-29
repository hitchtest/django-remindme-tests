Django-RemindMe-Test
====================

Django-RemindMe-Test is an example test + engine using hitch for use with the
example Django-RemindMe_ application.

To emphasize the isolation from the application itself, it's in a different
repository.

It's very easy to set up...

Set up
======

On Ubuntu::

    $ sudo apt-get install python python-virtualenv python-pip git firefox node-less automake libtool libreadline6 libreadline6-dev zlib1g-dev libxml2 libxml2-dev

And, to install the hitch bootstrapper::

    $ sudo pip install hitch

On Mac OS X, ensure that you have firefox installed, and then run::

    $ brew install python python3 git libtool automake npm

    $ npm install -g less

    $ pip install -U setuptools pip virtualenv hitch

First clone the django-remindme project, which contains the application this project will test::

  $ git clone https://github.com/hitchtest/django-remindme.git

Then, enter the Django-Remindme directory and clone this project inside it::

  $ git clone https://github.com/hitchtest/django-remindme-tests.git

Run
===

Enter the django-remindme/django-remindme-tests/ folder and run::

  $ hitch init

Then run::

  $ hitch test simple_reminder.test

Note that the first run of the test may take up to 20 minutes to run as it must download and build Redis, two pythons and Postgres.

Subsequent test runs will take seconds.

This command will run two tests - one *passing* test (with python 2.7) and one *failing* (with python 3.4).


Potential issues and caveats
============================

* The tests will only run on *nix systems. Windows is not supported.

* Sometimes the latest version of firefox does not work correctly with selenium. If you are experiencing selenium/firefox errors, try downgrading firefox one or two versions.


.. _Django-RemindMe: https://github.com/hitchtest/django-remindme
.. _pipsi: https://github.com/mitsuhiko/pipsi
