import datetime

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from graphos.renderers.morris import DonutChart, LineChart
from graphos.sources.simple import SimpleDataSource

from core.models import App
from telemetry.models import Signal, ActiveUsersCount


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
        return Signal.objects.filter(type__app=app).order_by("-received_at")[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        one_month_ago = datetime.date.today() - datetime.timedelta(days=30)
        one_week_ago = datetime.date.today() - datetime.timedelta(days=7)
        one_day_ago = datetime.date.today() - datetime.timedelta(days=1)

        app = App.objects.get(id=self.kwargs['app_id'], organization_id=self.request.user.ablatoruser.organization_id)
        app_signals = Signal.objects.filter(type__app=app)

        last_month_signals = app_signals.filter(received_at__gte=one_month_ago)
        last_week_signals = app_signals.filter(received_at__gte=one_week_ago)
        last_day_signals = app_signals.filter(received_at__gte=one_day_ago)

        distinct_last_month_signals = Signal.distinctivize(last_month_signals)

        context['active_users_last_month'] = len(distinct_last_month_signals)
        context['active_users_last_week'] = len(Signal.distinctivize(last_week_signals))
        context['active_users_last_day'] = len(Signal.distinctivize(last_day_signals))

        # Active User Count Graph
        range_date_end = datetime.date.today() - datetime.timedelta(days=1)
        range_date_beginning = range_date_end - datetime.timedelta(days=30)
        active_users_counts_data = [["Date", "User Count last 30 Days", "User Count last 7 Days", "User Count last Day"]]
        current_date = range_date_beginning
        while current_date < range_date_end:
            current_date += datetime.timedelta(days=1)
            active_users_counts_data.append([
                current_date.isoformat(),
                ActiveUsersCount.get(ending_at=current_date, day_range=30, app=app).count,
                ActiveUsersCount.get(ending_at=current_date, day_range=7, app=app).count,
                ActiveUsersCount.get(ending_at=current_date, day_range=1, app=app).count
            ])
        active_users_counts_data_source = SimpleDataSource(data=active_users_counts_data)
        context['active_monthly_users'] = LineChart(active_users_counts_data_source, width="100%")

        # Charts
        dim = 150
        context['charts'] = [
            {
                "App Version": DonutChart(accumulated_dictionary_data_source(distinct_last_month_signals, "appVersion"), height=dim,
                                          width=dim),
                "System Version": DonutChart(accumulated_dictionary_data_source(distinct_last_month_signals, "systemVersion"), height=dim,
                                             width=dim),
                "Build Number": DonutChart(accumulated_dictionary_data_source(distinct_last_month_signals, "buildNumber"), height=dim,
                                           width=dim),
                "Source Type": DonutChart(create_source_type_chart(distinct_last_month_signals), height=dim, width=dim),
            },
            {
                "Libido Description Type": DonutChart(
                    accumulated_dictionary_data_source(distinct_last_month_signals, "libidoDescriptionType"), height=dim, width=dim),
                "Should Send Notifications": DonutChart(
                    accumulated_dictionary_data_source(distinct_last_month_signals, "shouldSendExperienceSamplingNotifications"),
                    height=dim, width=dim),
                "Should Use HealthKit": DonutChart(accumulated_dictionary_data_source(distinct_last_month_signals, "shouldUseHealthKit"),
                                                   height=dim, width=dim),

            }
        ]
        return context
