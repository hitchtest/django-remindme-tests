Django-RemindMe-Test
====================

Django-RemindMe-Test is an example test + engine using hitch for use with the
example Django-RemindMe_ application.

To emphasize the isolation from the application itself, it's in a different
repository.

Setup
=====

You must have Postgresql, Redis, Python and Virtualenv installed before continuing.

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

  $ hitch test simple_reminder.yml

You may need to tweak some of the values in settings.yml to get it
to run on your machine - depending upon which versions of Postgres
and Redis you have installed, for instance.

Caveats
=======

* The tests will only run on *nix systems. Windows is not supported.


.. _Django-RemindMe: https://github.com/hitchtest/django-remindme
