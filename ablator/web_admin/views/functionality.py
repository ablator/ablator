from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from core.models import Functionality, App


@method_decorator(login_required, name='dispatch')
class FunctionalityDetail(TemplateView):
    template_name = 'core/functionality_detail.html'

    def get_context_data(self, pk, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['functionality'] = Functionality.objects.filter(
            app__organization=self.request.user.ablatoruser.organization).get(id=pk)
        return context_data


@method_decorator(login_required, name='dispatch')
class FunctionalityPartEnabledUsers(FunctionalityDetail):
    template_name = 'core/functionality/_enabled_users.html'


@method_decorator(login_required, name='dispatch')
class FunctionalityPartProgress(FunctionalityDetail):
    template_name = 'core/functionality/_progress.html'


@method_decorator(login_required, name='dispatch')
class FunctionalityPartFlavors(FunctionalityDetail):
    template_name = 'core/functionality/_flavors.html'


@method_decorator(login_required, name='dispatch')
class FunctionalityCreate(CreateView):
    model = Functionality
    fields = ['name', 'rollout_strategy']

    def form_valid(self, form):
        app_id = self.kwargs.get('pk')
        app = App.objects.get(id=app_id)
        form.instance.app = app
        form.instance.slug = slugify(form.instance.name)
        return super(FunctionalityCreate, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class FunctionalityUpdate(UpdateView):
    model = Functionality
    fields = ['name', 'slug', 'rollout_strategy']


@method_decorator(login_required, name='dispatch')
class FunctionalityDelete(DeleteView):
    model = Functionality
    success_url = reverse_lazy('home')
