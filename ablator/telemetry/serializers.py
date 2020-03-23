from rest_framework import serializers

from telemetry.models import SignalType, Signal


class SignalTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignalType
        fields = ["name"]


class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal
        fields = ["id", "received_at", "type", "user", "parameters"]
