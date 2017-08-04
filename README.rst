Ablator is a Functionality-Switching-Service that makes it easy for your app to roll out new
features in a controlled way, and to perform reliable A/B testing.
====================================================================================================

It works like this:

1. You define your app's switchable functionalities in ablator.
2. Your app asks ablator "Can I user X use Functionality Y?" and shows or hides the functionality
   as needed.
3. ablator takes care of slowly rolling out the feature in a way that you define.

As an administrator, you'll get a nice overview of what percentage of users has a functionality
enabled.

.. figure:: docs/screenshot.png
   :alt: Screen shot showing the percentage of enabled users for a functionality

At the moment, ablator is in an early stage of development. The core functionality, especially
APIs for funtionality checking, is there, but there are a lot of improvements to be made. See the
road map below for a list of features that are planned for the future.

Owing to the early stage, you'll probably have to have some experience in hosting a Django
application to be able to use ablator right now. It is planned to mitigate this in the future by
offering a version in a Docker container, or even as a service in some distant point in the future.
However, ablator will stay open source, because open source is cool and helpful!


Getting Started
---------------

Ablator's top concept is the *App*. An *App* can have multiple *Functionalities*, which are
individual features of your application that you want to manage in ablator. Not all of your app's
features have to be present in ablator, only those you want to manage and roll out in a controlled
way.

A *Functionality* can have one or more *Flavors*. If only one *Flavor* is present, the
*Functionality* is a binary affair: Either your users have it enabled, or not. If multiple
*Flavors* are present, you can present your users different variants of the same feature, e.g. for
use in A/B or Red/Green testing.

Defining Switchable Functionalities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Right now, you'll have to configure ablator entirely from the Django admin interface. A proper
web interface will follow as soon as possible.

To start, define a new *App*, giving it a name and a slug. The name is for use in the web interface,
whereas the slug identifies the feature to the API and client libraries. Add a few *Functionalities*
to your new app -- each *Functionality* should describe a distinct feature of your app. Give your
*Functionality* one *Flavor* (named, e.g., "on") to use ablator as a simple on/off switch. Give it
more *Flavors* to randomly distribute your users between them.

Here are some examples for *Functionalities* and *Flavors*:

- an intro screen that pops up to inform users about your app (one *Flavor* named "on")
- a new settings tab (one *Flavor* named ``full-settings``, one named ``simple-settings``)
- your app's new color scheme (*Flavors* named ``red``, ``green``, and ``blue``)

Rollout and Releases
~~~~~~~~~~~~~~~~~~~~

To roll out your new *Functionality*, you need to set a release strategy. Possible options are

:Recall Functionality:
    Oops, you made a mistake. All users will have that functionality revoked, even those who had it
    enabled in some form before.

:Pause Roll Out:
    All new users will get the functionality disabled, but users who already had the functionality
    will get to keep it.

:Enable Globally:
    Once you're satisfied the functionality works as intended and doesn't overwhelm your servers,
    use this roll out strategy to enable it for all users.

:As defined by Releases:
    During the rolling out process, it makes sense to have more fine-grained control over how your
    *Functionality* is enabled. Add one or more *Release* objects to your *Functionality* to
    configure those more fine-grained options.

A *Release*, in ablator terms, is a stretch of time that during which a certain set of rules 
are defined how many and which users should be allowed to get a *Flavor* switched on for them.
Right now, *Releases* can define a maximum number of users, which enables you to define slow
roll out. Ablator will only allow that many users to have the *Functionality* enabled, and will
randomly distribute them among the available *Flavors*. In the future, it's planned to make 
*Releases* even more configurable.

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

:http://example.com/api/caniuse/<user_string>/<functionality_id>/:
    This will return a boolean value indicating whether the functionality has any flavors that
    are enabled for the user. You can use this API endpoint if you expect a functionality
    which is only switched on or off using ablator.

:http://example.com/api/which/<user_string>/<functionality_id>/:
    This endpoint will return the full slug of the *Flavor* that is enabled for the user
    if any, or None otherwise. 

You can also use client libraries instead of accessing the API yourself. The ``karman``
directory contains an example library for Python projects, and more are planned.


Road Map
--------

These are the things that ablator doesn't have, but still needs. If you feel like something is
missing here, or a feature is especially important to you, please open a GitHub issue. It will be
greatly appreciated 🙂.

Client Libraries
~~~~~~~~~~~~~~~~

:Python:
    Already started. See the `karman` directory in this repository.

:Swift:
    Pending

:Your Favourite Language?:
    Open an issue and let me know!

Performance
~~~~~~~~~~~

A lot can be done here, simply optimizing the number of database calls, as well as moving to 
caching the results of calculations and request.

Web UI
~~~~~~

The web user interface for administrators is planned to reach these milestones:

1. The Web UI should be able to completely replace the admin interface. All actions regarding the 
   creation of Apps, Functionalities, Flavors, etc should be able to be done via a custom interface.
2. The Web UI should include helpful methods for releasing *right now* to a certain number of users,
   or other features to make the life of ablator users more comfortable.
3. Make the UI more interactive. Automatic reloading of data, separation of presentation and
   content, general ajaxyness.
4. Inclusion of various types of graphs (this goes hand in hand with the logging feature below) 
5. It should be beautiful.

Logging
~~~~~~~

There is a lot of live data that we don't want to save into the regular Django Database, but could
log into either Django's in memory cache, or something like redis. Logged data should include, among
other things, new users, recurring users, etc. Once the data is logged into temp storage, nice
graphs can be generated from it and displayed. Or it can be displayed live.

User Management
~~~~~~~~~~~~~~~

Django already has great user and permission management in the backend, so this is "just" a matter
of writing the appropriate views.

Dockerization
~~~~~~~~~~~~~

The goal for ablator is to make it as easy as possible to just drop into an existing infrastructure.
To that end, preparing a Docker container goes a long way.

More Roll Out Strategies
~~~~~~~~~~~~~~~~~~~~~~~~

Roll Out strategies and Releases could cover a lot of ways that developers and product owners want
to roll out individual functionalities. To that end, ablator needs a few more ways to configure a
release period. Some of those are:

- Distinguish Between App Versions
- Slowly grow up to a certain percentage of users enabled
- Let in x number of users, but not on first come first server but distributed over time

Test Coverage
~~~~~~~~~~~~~

Unit Tests are an important way to ensure that a code base has a certain level of maturity and
quality. Due to how ablator began, it has no tests whatsoever right now. After some slight
restructuring of the functionality code, it should be possible to reach a high level of code
coverage there.

Ablator As A Service
~~~~~~~~~~~~~~~~~~~~

Maybe some day, if people are interested, ablator can run on a hosted server for a small fee. This
does not go against it being open source though. Sentry, a project which ablator draws a lot of
inspiration from, also manages to bridge the gap between open source and commercial in a great way.

Help Out and Code of Conduct
----------------------------

We'd like to encourage your feature requests, bug reports and pull requests. Please note that a
Code of Conduct as described in `CODE_OF_CONDUCT.md` applies to this project. In short, be friendly,
welcoming, considerate, respectful, and be careful in the words that you choose please. If you think
you've witnessed a CoC violation, please contact Daniel at winsmith@winsmith.de .
