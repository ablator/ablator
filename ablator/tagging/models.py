import uuid
from django.db import models

from core.models import ClientUser
from user_management.models import Organization


class Tag(models.Model):
    """
    A trait, label, or group for a set of users.

    Tags can be used to categorize and group ClientUser objects into sub groups.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.SlugField()
    users = models.ManyToManyField(ClientUser)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'organization')

    def __str__(self):
        return 'Tag "{}" in Organization "{}"'.format(self.name, self.organization)
