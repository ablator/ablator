from django import forms

from core.models import RolloutStrategy, Functionality, Flavor
from tagging.models import Tag


class RolloutStrategyForm(forms.ModelForm):
    class Meta:
        model = RolloutStrategy
        fields = ["priority", "start_at", "possible_flavors", "max_enabled_users", "tag", "strategy", "functionality"]

    def __init__(self, functionality, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["possible_flavors"].queryset = Flavor.objects.filter(functionality=functionality)
        self.fields["functionality"].queryset = Functionality.objects.filter(id=functionality.id)
        self.fields["tag"].queryset = Tag.objects.filter(organization=functionality.app.organization)
