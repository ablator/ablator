import json
import datetime

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
                parameters = self.parameters.replace("'", '"').replace("True", "true").replace("False", "false")
                return json.loads(parameters)
            except json.JSONDecodeError:
                return {}

    @staticmethod
    def distinctivize(signals):
        distinct_user_signals = []
        known_users = []
        for signal in signals:
            if signal.user_id in known_users:
                continue
            known_users.append(signal.user_id)
            distinct_user_signals.append(signal)
        return distinct_user_signals


class ActiveUsersCount(models.Model):
    DAY_RANGE_CHOICES = ((1, "24 hours"), (7, "Week"), (30, "Month"))

    app = models.ForeignKey(App, on_delete=models.CASCADE)
    ending_at = models.DateField()
    day_range = models.IntegerField(choices=DAY_RANGE_CHOICES)
    count = models.IntegerField()

    @staticmethod
    def get(ending_at: datetime.date, day_range: int, app: App) -> "ActiveUsersCount":
        """Retrieve or create an ActiveUsersCount instance for the specified date and range"""

        active_users_count = None
        try:
            active_users_count = ActiveUsersCount.objects.get(app=app, ending_at=ending_at, day_range=day_range)
            return active_users_count
        except ActiveUsersCount.DoesNotExist:
            active_users_count = ActiveUsersCount(app=app, ending_at=ending_at, day_range=day_range)

        beginning_at = ending_at - datetime.timedelta(days=day_range)

        app_signals = Signal.objects.filter(type__app=app)
        range_signals = app_signals.filter(received_at__gte=beginning_at, received_at__lte=ending_at)
        distinct_signals = Signal.distinctivize(range_signals)
        active_users_count.count = len(distinct_signals)
        active_users_count.save()

        return active_users_count
