from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    """Groups users and apps"""
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.slug


class AblatorUser(models.Model):
    """Extension of the regular Django User Model with Ablator-Specific addons"""
    user = models.OneToOneField(User)
    company = models.ForeignKey(Company)

    def __str__(self):
        return self.user.username
