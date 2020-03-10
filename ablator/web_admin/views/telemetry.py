import datetime

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from telemetry.models import Signal
from core.models import ClientUser, App

from graphos.sources.simple import SimpleDataSource
from graphos.renderers.morris import DonutChart


def accumulated_dictionary_data_source(signals: list, signal_parameter_key: str) -> SimpleDataSource:
    counter = {}

    for signal in signals:
        value = signal.parameters_dict.get(signal_parameter_key, None)
        counter[value] = counter.get(value, 0) + 1

    data = [[signal_parameter_key, "Amount"]]

    for count_tuple in counter.items():
        data.append([str(count_tuple[0]), count_tuple[1]])
    data_source = SimpleDataSource(data=data)
    return data_source

def create_source_type_chart(signals):
    source_version_count = {
        "isTestFlight": 0,
        "isAppStore": 0,
        "isSimulator": 0
    }
    for signal in signals:
        isTestFlight = signal.parameters_dict.get("isTestFlight", False)
        isAppStore = signal.parameters_dict.get("isAppStore", False)
        isSimulator = signal.parameters_dict.get("isSimulator", False)

        if isTestFlight:
            source_version_count["isTestFlight"] += 1
        if isAppStore:
            source_version_count["isAppStore"] += 1
        if isSimulator:
            source_version_count["isSimulator"] += 1

    data = [["Source Type", "Amount"]]
    for app_version_count in source_version_count.items():
        data.append([str(app_version_count[0]), app_version_count[1]])
    return SimpleDataSource(data=data)


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
        one_day_ago = datetime.date.today() - datetime.timedelta(days=1)

        app = App.objects.filter(organization=self.request.user.ablatoruser.organization).get(id=self.kwargs['app_id'])
        app_signals = Signal.objects.filter(type__app=app)

        last_month_signals = app_signals.filter(received_at__gte=one_month_ago)
        last_week_signals = app_signals.filter(received_at__gte=one_week_ago)
        last_day_signals = app_signals.filter(received_at__gte=one_day_ago)

        last_month_users = ClientUser.objects.filter(signal__in=last_month_signals).distinct()
        last_week_users = last_month_users.filter(signal__in=last_week_signals).distinct()
        last_day_users = last_month_users.filter(signal__in=last_day_signals).distinct()

        context['active_users_last_month'] = last_month_users.count()
        context['active_users_last_week'] = last_week_users.count()
        context['active_users_last_day'] = last_day_users.count()

        # Charts
        dim = 150
        distinct_user_signals = []
        known_users = []

        for signal in last_month_signals:
            if signal.user in known_users:
                continue
            known_users.append(signal.user)
            distinct_user_signals.append(signal)

        context['charts'] = [{
            "App Version": DonutChart(accumulated_dictionary_data_source(distinct_user_signals, "appVersion"), height=dim, width=dim),
            "System Version": DonutChart(accumulated_dictionary_data_source(distinct_user_signals, "systemVersion"), height=dim, width=dim),
            "Build Number": DonutChart(accumulated_dictionary_data_source(distinct_user_signals, "buildNumber"), height=dim, width=dim),
            "Source Type": DonutChart(create_source_type_chart(distinct_user_signals), height=dim, width=dim),
        },
        {
            "Libido Description Type": DonutChart(accumulated_dictionary_data_source(distinct_user_signals, "libidoDescriptionType"), height=dim, width=dim),
            "Should Send Notifications": DonutChart(accumulated_dictionary_data_source(distinct_user_signals, "shouldSendExperienceSamplingNotifications"), height=dim, width=dim),
            "Should Use HealthKit": DonutChart(accumulated_dictionary_data_source(distinct_user_signals, "shouldUseHealthKit"), height=dim, width=dim),

        }]
        return context
