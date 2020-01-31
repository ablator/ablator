from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from telemetry.models import Signal


@method_decorator(login_required, name='dispatch')
class SignalListView(ListView):
    template_name = "telemetry/signal_list.html"

    def get_queryset(self):
        app = App.objects.filter(organization=self.request.user.ablatoruser.organization).get(id=self.kwargs['app_id'])
        return Signal.objects.filter(app=app)
