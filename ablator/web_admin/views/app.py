from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.models import App


@method_decorator(login_required, name='dispatch')
class AppDetail(TemplateView):
    template_name = 'core/app_detail.html'

    def get_context_data(self, app_id, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['app'] = App.objects.filter(organization=self.request.user.ablatoruser.organization).get(id=app_id)
        return context_data


@method_decorator(login_required, name='dispatch')
class AppUsage(AppDetail):
    template_name = 'core/app_usage.html'


@method_decorator(login_required, name='dispatch')
class AppCreate(CreateView):
    model = App
    fields = ['name']

    def form_valid(self, form):
        form.instance.organization = self.request.user.ablatoruser.organization
        form.instance.slug = slugify(form.instance.name)
        return super(AppCreate, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class AppUpdate(UpdateView):
    model = App
    fields = ['name', 'slug']


@method_decorator(login_required, name='dispatch')
class AppDelete(DeleteView):
    model = App
    success_url = reverse_lazy('home')
