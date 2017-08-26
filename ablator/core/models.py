import hashlib
import uuid

from django.conf import settings
from django.db import models
from django.urls.base import reverse_lazy
from django.utils import timezone

from core.colors import random_color
from user_management.models import Organization

HASH_SALT = settings.HASH_SALT


class ClientUser(models.Model):
    """
    A user of the software.

    Users are always anonymized and only represented by a hash
    value, so privacy can be guaranteed.

    Hashing will use the provided object's __repr__ method, so please
    make sure that the __repr__ method outputs a value that is unique to
    the user and unchanging.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(Organization)

    def __str__(self):
        return '{}.{}'.format(self.organization, self.slug)

    def get_absolute_url(self):
        return reverse_lazy('app-detail', kwargs={'app_id': self.id})


class Functionality(models.Model):
    """
    A behaviour, functionality, or program option to be managed.

    A Functionality contains one or more Flavor objects that represent individual
    variations of one functionality. This is helpful when you want to A/B test multiple
    incarnations of a functionality.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    app = models.ForeignKey(App)

    RECALL_FUNCTIONALITY = 'recall'
    PAUSE_ROLLOUT = 'pause_rollout'
    DEFINED_BY_RELEASES = 'defined_by_releases'
    ENABLE_GLOBALLY = 'enable_globally'
    NEW_USER_BEAHAVIOUR_CHOICES = (
        (RECALL_FUNCTIONALITY, 'Recall'),
        (PAUSE_ROLLOUT, 'Roll Out Paused'),
        (DEFINED_BY_RELEASES, 'Release-Driven'),
        (ENABLE_GLOBALLY, 'Enabled Globally')
    )
    rollout_strategy = models.CharField(
        max_length=50,
        choices=NEW_USER_BEAHAVIOUR_CHOICES,
        default=DEFINED_BY_RELEASES
    )

    def __str__(self):
        return '{}.{}'.format(self.app, self.slug)

    class Meta:
        verbose_name_plural = "Functionalities"

    @property
    def number_of_users(self):
        return Availability.objects.filter(
            flavor__functionality=self
        ).count()

    @property
    def number_of_enabled_users(self):
        return Availability.objects.filter(
            flavor__functionality=self,
            is_enabled=True
        ).count()

    @property
    def current_release(self) -> 'Release':
        return self.release_set.filter(start_at__lte=timezone.now()).order_by('-start_at').first()

    def get_absolute_url(self):
        return reverse_lazy('functionality-detail', kwargs={'pk': self.id})


class Flavor(models.Model):
    """
    A specific version of a functionality.

    Add more then one Flavor to a Functionality to A/B test. One will be randomly
    activated depending on its enable_probability.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=100)
    functionality = models.ForeignKey(Functionality)
    client_users = models.ManyToManyField(ClientUser, through='Availability')
    color = models.CharField(max_length=6, default=random_color)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}.{}".format(self.functionality, self.slug)

    @property
    def number_of_users(self):
        return self.availability_set.count()

    @property
    def number_of_enabled_users(self):
        return self.availability_set.filter(is_enabled=True).count()

    @property
    def number_of_disabled_users(self):
        return self.availability_set.filter(is_enabled=False).count()

    @property
    def single_width_percent(self):
        try:
            return float(self.number_of_enabled_users) / self.number_of_users * 100
        except ZeroDivisionError:
            return 1 * 100

    @property
    def width_percent(self):
        try:
            return float(self.number_of_enabled_users) / self.functionality.number_of_users * 100
        except ZeroDivisionError:
            return 1 * 100

    def get_absolute_url(self):
        return reverse_lazy('functionality-detail', kwargs={'pk': self.functionality.id})


class Release(models.Model):
    """
    A point in time when a certain number of Availabilities should be switched on.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    functionality = models.ForeignKey(Functionality)
    start_at = models.DateTimeField(default=timezone.now)
    max_enabled_users = models.IntegerField(default=0)

    class Meta:
        ordering = ['start_at']

    @property
    def is_past(self) -> bool:
        return self.start_at < timezone.now() and self.functionality.current_release != self

    @property
    def is_current(self) -> bool:
        return self.functionality.current_release == self

    def get_absolute_url(self):
        return reverse_lazy('functionality-detail', kwargs={'pk': self.functionality.id})


class Availability(models.Model):
    """
    A Flavor that is enabled for a specific user.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    flavor = models.ForeignKey(Flavor, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}.{}".format(self.flavor, self.user)

    class Meta:
        verbose_name_plural = "Availabilities"
