import datetime

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from telemetry.models import Signal
from core.models import ClientUser, App


@method_decorator(login_required, name='dispatch')
class SignalListView(ListView):
    template_name = "telemetry/signal_list.html"

    def get_queryset(self):
        app = App.objects.filter(organization=self.request.user.ablatoruser.organization).get(id=self.kwargs['app_id'])
        return Signal.objects.filter(type__app=app).order_by("-received_at")[:200]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        one_month_ago = datetime.date.today() - datetime.timedelta(days=30)
        one_week_ago = datetime.date.today() - datetime.timedelta(days=7)

        app = App.objects.filter(organization=self.request.user.ablatoruser.organization).get(id=self.kwargs['app_id'])
        app_signals = Signal.objects.filter(type__app=app)

        last_month_signals = app_signals.filter(received_at__gte=one_month_ago)
        last_week_signals = app_signals.filter(received_at__gte=one_week_ago)

        last_month_users = ClientUser.objects.filter(signal_set__in=last_month_signals)
        last_week_users = ClientUser.objects.filter(signal_set__in=last_week_signals)

        context['active_users_last_month'] = last_month_users.count()
        context['active_users_last_week'] = last_week_users.count()

        return context
