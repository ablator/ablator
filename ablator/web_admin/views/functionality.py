from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from core.models import Functionality


@method_decorator(login_required, name='dispatch')
class FunctionalityDetail(TemplateView):
    template_name = 'functionality.html'

    def get_context_data(self, functionality_id, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['functionality'] = Functionality.objects.filter(app__company=self.request.user.ablatoruser.company).get(id=functionality_id)
        return context_data