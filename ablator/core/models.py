from django.db import models
from django.conf import settings

import hashlib

HASH_SALT = settings.FEATURE_HASH_SALT


class User(models.Model):
    """Represents a user of the software.

    Users are always anonymized and only represented by a hash
    value, so privacy can be guaranteed.

    Hashing will use the provided object's __repr__ method, so please
    make sure that the __repr__ method outputs a value that is unique to
    the user and unchanging.
    """
    name = models.CharField(max_length=255)

    def __repr__(self):
        return self.name

    @classmethod
    def user_from_object(cls, user_object):
        user_hash = cls.hash_from_object(user_object)
        instance, created = cls.objects.get_or_create(name=user_hash)
        return instance

    @classmethod
    def hash_from_object(cls, hashable_object):
        return hashlib.sha256(HASH_SALT.encode() + str(hashable_object).encode()).hexdigest()


class Functionality(models.Model):
    """
    behaviour, functionality, program option
    """
    name = models.CharField(max_length=255)
    options = []  # list of strings


class Availability(models.Model):
    user = models.ForeignKey(User)
    functionality = models.ForeignKey(Functionality)
    enabled_index = None  # or an integer
