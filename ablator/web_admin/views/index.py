from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from core.models import App, Functionality, Flavor, Availability
from user_management.models import AblatorUser, Organization


@method_decorator(login_required, name='dispatch')
class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['apps'] = App.objects.filter(organization=self.request.user.ablatoruser.organization)
        return context_data


class StatusView(TemplateView):
    template_name = 'status.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['number_of_organizations'] = Organization.objects.all().count()
        context_data['number_of_users'] = AblatorUser.objects.all().count()
        context_data['number_of_apps'] = App.objects.all().count()
        context_data['number_of_functionalities'] = Functionality.objects.all().count()
        context_data['number_of_flavors'] = Flavor.objects.all().count()
        context_data['number_of_availabilities'] = Availability.objects.all().count()
        return context_data
