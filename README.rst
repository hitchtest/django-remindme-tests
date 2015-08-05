Django-RemindMe-Test
====================

Django-RemindMe-Test is an example test + engine using hitch for use with the
example Django-RemindMe_ application.

To emphasize the isolation from the application itself, it's in a different
repository.

It's very easy to set up...

Set up on Mint/Ubuntu/Debian
----------------------------

Run the following::

    $ sudo apt-get install python3 python-setuptools python3-dev python-virtualenv python-pip git node-less automake libtool patch libreadline6 libreadline6-dev zlib1g-dev libxml2 libxml2-dev make build-essential libssl-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libpq-dev iceweasel xvfb xauth xserver-xorg

    $ sudo pip install hitch


Set up on Red Hat/CentOS/Fedora
-------------------------------

On CentOS make sure that python3 is installed, e.g.::

    $ sudo yum install https://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/ius-release-1.0-14.ius.centos6.noarch.rpm

    $ sudo yum install python34u

On Fedora::

    $ sudy yum install python3 python3-devel

And then::

    $ sudo yum install python-setuptools python-devel python-pip python-virtualenv git firefox nodejs-less automake libtool patch readline-devel zlib-devel libxml2 libxml2-devel gcc gcc-c++ make openssl-devel bzip2-libs zlib-devel bzip2-devel sqlite-devel wget curl llvm postgresql-libs postgresql-devel xhost xorg-x11-xauth xorg-x11-server-Xvfb

    $ sudo pip install hitch


Set up on Arch
--------------

Run the following::

    $ sudo pacman -S python3 python-setuptools python-pip python-virtualenv m4 base-devel git firefox xorg-xauth xorg-xhost firefox nodejs-less automake readline zlib libxml2 gcc make openssl bzip2 zlib sqlite3 wget curl llvm postgresql-libs xorg-server-xvfb

    $ sudo pip install hitch


Set up on Mac OS X
------------------

On Mac OS X, ensure that you have firefox installed, and then run::

    $ brew install python python3 git libtool automake npm readline

    $ brew link readline

    $ npm install -g less

    $ pip install -U setuptools pip virtualenv hitch


Download the Project and Run
============================

First clone the django-remindme project, which contains the application this project will test, and then clone this tests repo inside it::

  $ git clone --recursive https://github.com/hitchtest/django-remindme.git

  $ cd django-remindme/django-remindme-tests

Note the --recursive is necessary because this project is a submodule of django-remindme.


Run
---

Once in the django-remindme/django-remindme-tests/ folder, run::

  $ hitch init

Then run::

  $ hitch test simple_reminder.test

Note that the *first* run of the test may take up to 20 minutes to run as it must download and build Redis, two pythons and Postgres.

This command will run the same test in python 2.7.10 and python 3.4.3. Both should pass.

While waiting, this might be good time to:

* Follow hitch on twitter: @testhitch
* Subscribe to the subreddit: /r/hitchtest

If you see *any* failure when running these tests after installing the relevant packages, *please* raise an issue at
https://github.com/hitchtest/django-remindme-tests or email colm.oconnor.github@gmail.com.


Potential issues and caveats
----------------------------

* Some environments may have problems building python, redis and postgres due to necessary packages not being installed. Please notify me if this happens to you.

* The tests will only run on *nix systems. Windows is not supported.


.. _Django-RemindMe: https://github.com/hitchtest/django-remindme
.. _pipsi: https://github.com/mitsuhiko/pipsi
