

Road Map
========

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