from decimal import Decimal
from django.db import models
from django.conf import settings

import hashlib

HASH_SALT = settings.FEATURE_HASH_SALT


class ClientUser(models.Model):
    """
    A user of the software.

    Users are always anonymized and only represented by a hash
    value, so privacy can be guaranteed.

    Hashing will use the provided object's __repr__ method, so please
    make sure that the __repr__ method outputs a value that is unique to
    the user and unchanging.
    """
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @classmethod
    def user_from_object(cls, user_object):
        user_hash = cls.hash_from_object(user_object)
        instance, created = cls.objects.get_or_create(name=user_hash)
        return instance

    @classmethod
    def hash_from_object(cls, hashable_object):
        return hashlib.sha256(HASH_SALT.encode() + str(hashable_object).encode()).hexdigest()


class App(models.Model):
    """
    A collection of FunctionalityGroups.
    """
    name = models.SlugField(max_length=100)
    human_readable_name = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class FunctionalityGroup(models.Model):
    """
    A behaviour, functionality, or program option to be managed.

    A FunctionalityGroup contains one or more Functionality objects that represent individual
    variations of one functionality. This is helpful when you want to A/B test multiple
    incarnations of a functionality.
    """
    name = models.SlugField(max_length=100)
    human_readable_name = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    app = models.ForeignKey(App)

    RECALL_FEATURE = 'recall_feature'
    PAUSE_ROLLOUT = 'pause_rollout'
    DEFINED_BY_RELEASES = 'defined_by_releases'
    ENABLE_GLOBALLY = 'enable_globally'
    NEW_USER_BEAHAVIOUR_CHOICES = (
        (RECALL_FEATURE, 'Recall Feature'),
        (PAUSE_ROLLOUT, 'Pause Roll Out'),
        (DEFINED_BY_RELEASES, 'As defined by Releases'),
        (ENABLE_GLOBALLY, 'Enable Globally')
    )
    rollout_strategy = models.CharField(
        max_length=50,
        choices=NEW_USER_BEAHAVIOUR_CHOICES,
        default=DEFINED_BY_RELEASES
    )

    def __str__(self):
        return '{}.{}'.format(self.app, self.name)


class Functionality(models.Model):
    """
    A specific version of a functionality.

    Add more then one Functionality to a FunctionalityGroup to A/B test. One will be randomly
    activated depending on its enable_probability.
    """
    name = models.SlugField(max_length=100)
    human_readable_name = models.CharField(max_length=140)
    group = models.ForeignKey(FunctionalityGroup)
    client_users = models.ManyToManyField(ClientUser, through='Availability')
    color = models.CharField(max_length=6, default='c0ffee')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}.{}".format(self.group, self.name)

    class Meta:
        verbose_name_plural = "Functionalities"

    @property
    def current_release(self) -> 'Release':
        raise NotImplementedError


class Release(models.Model):
    """
    A point in time when a certain number of Availabilities should be switched on.
    """
    functionality_group = models.ForeignKey(FunctionalityGroup)
    name = models.CharField(max_length=100, blank=True)
    start_at = models.DateTimeField(null=True)
    end_at = models.DateTimeField(null=True)
    enabled_users = models.IntegerField(default=0)

    @property
    def is_current(self) -> bool:
        raise NotImplementedError


class Availability(models.Model):
    """
    A Functionality that is enabled for a specific user.
    """
    user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    functionality = models.ForeignKey(Functionality, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}.{}".format(self.functionality, self.user)

    class Meta:
        verbose_name_plural = "Availabilities"
