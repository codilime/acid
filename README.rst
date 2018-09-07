ACID CI DASHBOARD
=================

ACID CI Dashboard is an open source user interface for Zuul Gating system.
More information about Zuul Gating system you can find at: https://zuul-ci.org/docs/zuul/

ACID CI Dashboard is under APACHE 2.0 LICENSE, for more info check LICENSE.

TOOLS AND LIBRARIES NEEDED
--------------------------

ACID requires Python 3.6.x. and Python3.6-venv.
Please make sure you have `Python 3.6` and `Python 3.6-venv` version in your OS.

For creating virtual enviroment `Ansible` and `Vagrant` tools are used. Make sure you have these installed as well as `libvirt` library.


HOW TO INSTALL
--------------

Create new virtual environment and install all dependencies

.. code:: console

   $ make venv
   $ . .venv/bin/activate

Run vagrant for remote services like Zuul and Gerrit for development purposes.

.. code:: console

    $ make dev-run

After starting up Vagrant machine wait arount 30-40 seconds for Zuul and Gerrit services to properly load.

RUN ACID
--------

.. code:: console

    $ source .venv/bin/activate
    $ make serve

Server will listen on http://127.0.0.1:3000/

RUN TESTS
---------

Run unit tests or integration tests separately.

.. code:: console

    $ . .venv/bin/activate
    $ make test-unit
    $ make test-integration

Run all tests cases

.. code:: console

    $ . .venv/bin/activate
    $ make test

Run PEP8 linter

.. code:: console

    $ . .venv/bin/activate
    $ make lint

You can also use tox to run tests against Python 3.6 and 3.7

.. code:: console

    $ . .venv/bin/activate
    $ tox

