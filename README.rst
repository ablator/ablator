Ablator is a Functionality-Switching-Service that makes it easy for your app to roll out new features in a controlled way, and to perform reliable A/B testing.
===========

.. image:: ablator/web_admin/static/ablator/ablator_logo.png
   :align: center

It works like this:

1. You define your app's switchable functionalities in ablator.
2. Your app asks ablator "User X wants Functionality Y. Which Flavor should I show them, if any?"
3. ablator takes care of slowly rolling out the feature in a way that you define.

As an administrator, you'll get a nice overview of what percentage of users has a functionality
enabled.

.. figure:: docs/screenshot.png
   :alt: Screen shot showing the percentage of enabled users for a functionality

At the moment, ablator is in an early stage of development. The core APIs are completely available,
and there is a custom user interface to manage day-to-day operations. There is also a Docker
file available, so you can deploy it yourself.

See the `road map`_ for a list of features that are planned for the future.

.. _road map: docs/roadmap.rst

For an in-depth explanation of the logical parts of ablator, see the `models description`_.

.. _models description: docs/models.rst

Accessing the Ablator API
~~~~~~~~~~~~~~~~~~~~~~~~~

When the ablator server is running, it exposes two API endpoints, named ``which`` and 
``caniuse``. Both take a user-identifier and a functionality id. The identifier can be any
string that identifies your users between launches of your app, e.g. a user ID, an email 
address, etc. It will be hashed before being saved to the ablator database. The
functionality id can be obtained from the admin interface. We don't use functionality
slugs in the URL to make it harder for people who listen to your app's web traffic to find 
out which functionalities (that might still be in development even) are theoretically 
available.

http://example.com/api/v1/caniuse/<user_string>/<functionality_id>/
    This will return a boolean value indicating whether the functionality has any flavors that
    are enabled for the user. You can use this API endpoint if you expect a functionality
    which is only switched on or off using ablator.

http://example.com/api/v1/which/<user_string>/<functionality_id>/
    This endpoint will return the full slug of the *Flavor* that is enabled for the user
    if any, or None otherwise. 

You can also use client libraries instead of accessing the API yourself. The ``karman``
directory contains an example library for Python projects, and more are planned.


Help Out and Code of Conduct
----------------------------

We'd like to encourage your feature requests, bug reports and pull requests. Please note that a
Code of Conduct as described in `CODE_OF_CONDUCT.md` applies to this project. In short, be friendly,
welcoming, considerate, respectful, and be careful in the words that you choose please. If you think
you've witnessed a CoC violation, please contact Daniel at winsmith@winsmith.de .
