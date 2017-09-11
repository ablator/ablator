from django.contrib.auth.models import User
from django.db import models


class Organization(models.Model):
    """Groups users and apps"""
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug


class AblatorUser(models.Model):
    """Extension of the regular Django User Model with Ablator-Specific addons"""
    user = models.OneToOneField(User)
    organization = models.ForeignKey(Organization)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
