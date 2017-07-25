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
    name = models.CharField(max_length=140)
    fqdn = models.CharField(max_length=140)
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
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    app = models.ForeignKey(App)

    def __str__(self):
        return self.name


class Functionality(models.Model):
    """
    A specific version of a functionality.

    Add more then one Functionality to a FunctionalityGroup to A/B test. One will be randomly
    activated depending on its enable_probability.
    """
    name = models.CharField(max_length=255)
    group = models.ForeignKey(FunctionalityGroup)
    client_users = models.ManyToManyField(ClientUser, through='Availability')
    enable_probability = models.DecimalField(default=Decimal('0'), decimal_places=6, max_digits=7)
    color = models.CharField(max_length=6, default='c0ffee')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} => {}".format(self.group, self.name)

    class Meta:
        verbose_name_plural = "Functionalities"


class Availability(models.Model):
    """
    A Functionality that is enabled for a specific user.
    """
    user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    functionality = models.ForeignKey(Functionality, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "User {} has functionality {}".format(self.user, self.functionality)

    class Meta:
        verbose_name_plural = "Availabilities"

