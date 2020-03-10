import json

from django.db import models
from core.models import ClientUser, App


class SignalType(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    app = models.ForeignKey(App, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Signal(models.Model):
    received_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    type = models.ForeignKey(SignalType, on_delete=models.CASCADE)
    parameters = models.TextField()

    @property
    def parameters_dict(self):
        try:
            return json.loads(self.parameters)
        except json.JSONDecodeError:
            # A previous version saved python dict strings instead of JSON, try to convert on the fly
            try:
                parameters = self.parameters.replace("'", "\"").replace("True", "true").replace("False", "false")
                return json.loads(parameters)
            except json.JSONDecodeError:
                return {}

