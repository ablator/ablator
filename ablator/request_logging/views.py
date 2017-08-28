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
        for timestamp_key in timestamp_keys:
            if pk in timestamp_key:
                logs[timestamp_key] = get_request_logs(timestamp_key)
        context['logs'] = logs
        return context
