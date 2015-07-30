Django-RemindMe-Test
====================

Django-RemindMe-Test is an example test + engine using hitch for use with the
example Django-RemindMe_ application.

To emphasize the isolation from the application itself, it's in a different
repository.

It's very easy to set up...

Set up on Ubuntu
----------------

Run the following::

    $ sudo apt-get install python3 python-setuptools python3-dev python-virtualenv python-pip git firefox node-less automake libtool libreadline6 libreadline6-dev zlib1g-dev libxml2 libxml2-dev make build-essential libssl-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libpq-dev

    $ sudo pip install hitch

Set up on Red Hat/CentOS/Fedora
-------------------------------

Make sure python 3 is installed, e.g.::

    $ sudo yum install https://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/ius-release-1.0-14.ius.centos6.noarch.rpm

    $ sudo yum install python34u

And then::

    $ sudo yum install python-setuptools python-devel python-pip python-virtualenv git firefox nodejs-less automake libtool readline-devel zlib-devel libxml2 libxml2-devel gcc gcc-c++ make openssl-devel bzip2-libs zlib-devel sqlite-devel wget curl llvm postgresql-libs postgresql-devel xorg-x11-xauth

    $ sudo pip install hitch


Set up on Arch
--------------

    $ sudo pacman -S python3 python-setuptools python-pip python-virtualenv m4 base-devel git firefox xorg-xauth xorg-xhost firefox nodejs-less automake readline zlib libxml2 gcc make openssl bzip2 zlib sqlite3 wget curl llvm postgresql-libs

    $ sudo pip install hitch

Set up on Mac OS X
------------------

On Mac OS X, ensure that you have firefox installed, and then run::

    $ brew install python python3 git libtool automake npm readline

    $ brew link readline

    $ npm install -g less

    $ pip install -U setuptools pip virtualenv hitch


Download and Run
================

First clone the django-remindme project, which contains the application this project will test::

  $ git clone https://github.com/hitchtest/django-remindme.git

Then, enter the Django-Remindme directory and clone this project inside it::

  $ git clone https://github.com/hitchtest/django-remindme-tests.git

Run
---

Enter the django-remindme/django-remindme-tests/ folder and run::

  $ hitch init

Then run::

  $ hitch test simple_reminder.test

Note that the first run of the test may take up to 20 minutes to run as it must download and build Redis, two pythons and Postgres.

Subsequent test runs will take seconds.

This command will run two tests - one *passing* test (with python 2.7) and one *failing* (with python 3.4).


Potential issues and caveats
----------------------------

* The tests will only run on *nix systems. Windows is not supported.

* Sometimes the latest version of firefox does not work correctly with selenium. If you are experiencing selenium/firefox errors, try downgrading firefox one or two versions.


.. _Django-RemindMe: https://github.com/hitchtest/django-remindme
.. _pipsi: https://github.com/mitsuhiko/pipsi
