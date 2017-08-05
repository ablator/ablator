from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from core.models import App, Functionality


@method_decorator(login_required, name='dispatch')
class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['apps'] = App.objects.all()
        return context_data

class AppView(TemplateView):
    template_name = 'app.html'

    def get_context_data(self, app_id, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['app'] = App.objects.get(id=app_id)
        return context_data

class FunctionalityView(TemplateView):
    template_name = 'functionality.html'

    def get_context_data(self, functionality_id, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['functionality'] = Functionality.objects.get(id=functionality_id)
        return context_data
