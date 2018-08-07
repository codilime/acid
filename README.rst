AWESOME CI DASHBOARD (ACID)
===========================

Awesome CI Dashboard is an open source user interface for Zuul Gating system.

More information about Zuul Gating system you can find at:

https://zuul-ci.org/docs/zuul/

Project is currently in development stage and only works in a development environment.

Awesome CI Dashboard uses APACHE 2.0 LICENSE, for more info check LICENSE.

HOW TO INSTALL
--------------

ACID require Python 3.6.x. and Python3.6-venv  Please make sure you have Python 3.6 and Python 3.6 version in your OS.
If not install it before running project.


Create new virtual environment for ACID project, unless you don't care about PIP packages collision.

.. code:: console

   $ python3.6 -m venv .venv
   $ source .venv/bin/activate
   $ pip install setuptools wheel
   $ make install-dev

Run vagrant for remote services like Zuul and Gerrit for development purposes.

.. code:: console

    $ make dev-run


Run ACID
--------


.. code:: console

    $ source .venv/bin/activate
    $ make serve

Server will listen on http://127.0.0.1:3000/

RUN TESTS
---------

Enter ACID directory

.. code:: console

    $ source .venv/bin/activate
    $ make test && make lint

