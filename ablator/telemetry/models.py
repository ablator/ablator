from django.db import models
from core.models import ClientUser, App


class SignalType(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE)


class Signal(models.Model):
    user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    type = models.ForeignKey(SignalType, on_delete=models.CASCADE)
    parameters = models.TextField()
