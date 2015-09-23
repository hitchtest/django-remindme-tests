Django-RemindMe-Test
====================

Django-RemindMe-Test is an example test + engine using hitch for use with the
example Django-RemindMe_ application.


Install and Run Tests
=====================

There is a three step process to install and run the tests::

  $ git clone --recursive https://github.com/hitchtest/django-remindme.git

  $ cd django-remindme/django-remindme-tests

  $ curl -sSL https://hitchtest.com/init.sh > init.sh ; chmod +x init.sh ; ./init.sh

This script has been tested on, and supports, Debian, Ubuntu, Arch, Fedora and Mac OS X.

See also: https://hitchtest.readthedocs.org/en/latest/faq/what_does_the_init_script_do.html


Mac OS X pre-installation steps
-------------------------------

On Mac OS X, you must also first manually perform a couple of steps::

    1) Download and install firefox

    2) brew install npm ; npm install -g less


Known Issues
------------

* On Fedora 20: "curl https://hitchtest.com/init.sh" fails with "curl: (35) Cannot communicate securely with peer: no common encryption algorithm(s)". Use wget instead.

* On some Linux distributions running in a VM: the message "log timeout appears". This is likely caused by the timezone being set incorrectly.

* On some Linux distributions the site appears unstyled. This is due to a bug with libfaketime running with node-less. See: https://github.com/wolfcw/libfaketime/issues/63 (no fix available yet)


.. _Django-RemindMe: https://github.com/hitchtest/django-remindme
.. _pipsi: https://github.com/mitsuhiko/pipsi
