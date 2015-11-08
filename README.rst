===============================
Inspectors
===============================

Allows users to give customer service feedback to inspectors after recent inspections.

Status
------
Pre-Alpha. This was a stretch goal of the Fellows Team with the expectation to complete thisby the county or through Code for Miami, the local volunteer brigade.


Who Built This?
---------------
Ernie Hsiung of the 2015 Miami-Dade Fellows Team and Ben Golder of the 2015 RVA Fellows Team. Additional input from Mathias Gibson, Michael Sarasti (Miami-Dade County) and Christa Erml-Martinez (Miami-Dade County).


Overview
--------

User interface which allows users to enter a Miami-Dade County permit number and an e-mail address or a phone number, sending a customer experience survey to users when an inspection has been completed.

At regular intervals we will check the Miami-Dade County inspection routes and results tables, a copy of which is available on the Miami-Dade Open Data portal. If there is a match between a registered permit number and a recent inspection, a customizable survey about the users experiences with the inspector will be sent via e-mail or SMS.

The Typeform.IO generated survey hits a webhook on the codeforamerica/mdc-inspectors-dashboard repo when the survey is completed, and stakeholders and the public can view the dashboard there for results.


To Do
-----
* [ ] Generate the SMS message using Twilio.
* [ ] Build the mail script


Third-Party Platforms used
--------------------------

* Typeform.IO: To build dynamic, customizable surveys
* Sendgrid: The mail platform in the production environment. For development purposes we will be using Google Mail.
* Twilio: The hope is that to build the SMS component we will use the Twilio platform to send text messages.


Quickstart
----------

First, set your app's secret key as an environment variable. For example, example add the following to ``.bashrc`` or ``.bash_profile``.

.. code-block:: bash

    export INSPECTORS_SECRET='something-really-secret'


Then run the following commands to bootstrap your environment.


::

    git clone https://github.com/ErnieAtLYD/inspectors
    cd inspectors
    pip install -r requirements/dev.txt
    python manage.py server

You will see a pretty welcome screen.

Once you have installed your DBMS, run the following to create your app's database tables and perform the initial migration:

::

    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    python manage.py server



Deployment
----------

In your production environment, make sure the ``INSPECTORS_ENV`` environment variable is set to ``"prod"``.


Shell
-----

To open the interactive shell, run ::

    python manage.py shell

By default, you will have access to ``app``, ``db``, and the ``User`` model.


Running Tests
-------------

To run all tests, run ::

    python manage.py test


Migrations
----------

Whenever a database migration needs to be made. Run the following commands:
::

    python manage.py db migrate

This will generate a new migration script. Then run:
::

    python manage.py db upgrade

To apply the migration.

For a full migration command reference, run ``python manage.py db --help``.
