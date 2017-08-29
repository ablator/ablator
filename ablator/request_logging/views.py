from django.views.generic.base import TemplateView

from request_logging.logging import list_timestamp_keys, get_request_logs


class LogList(TemplateView):
    template_name = 'availability_logging/log.html'

    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        timestamp_keys = list_timestamp_keys()

        if not timestamp_keys:
            return context
        logs = {}
        newest_timestamp_key = max(filter(lambda x: pk in x, timestamp_keys))
        logs = reversed(get_request_logs(newest_timestamp_key))
        context['logs'] = logs
        return context
