
Ablator Model Structure
=======================

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
