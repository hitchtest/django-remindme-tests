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

* This error occurs on Mac OS X but can be safely ignored::

    Running setup.py bdist_wheel for pyuv
    Complete output from command /Users/vagrant/django-remindme/django-remindme-tests/.hitch/virtualenv/bin/python3.4 -c "import setuptools;__file__='/private/var/folders/wr/g_dl81tn5_x0t_yz3jw602cr0000gn/T/pip-build-8ifkjs8u/pyuv/setup.py';exec(compile(open(__file__).read().replace('\r\n', '\n'), __file__, 'exec'))" bdist_wheel -d /var/folders/wr/g_dl81tn5_x0t_yz3jw602cr0000gn/T/tmpd7m59gn2pip-wheel-:
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "/private/var/folders/wr/g_dl81tn5_x0t_yz3jw602cr0000gn/T/pip-build-8ifkjs8u/pyuv/setup.py", line 1
        ﻿# coding=utf-8
        ^
    SyntaxError: invalid character in identifier

    ----------------------------------------
    Failed building wheel for pyuv
    Failed to build pyuv

.. _Django-RemindMe: https://github.com/hitchtest/django-remindme
.. _pipsi: https://github.com/mitsuhiko/pipsi
