from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from core.models import Flavor, Functionality


@method_decorator(login_required, name='dispatch')
class FlavorCreate(CreateView):
    model = Flavor
    fields = ['name', 'color']

    def form_valid(self, form):
        functionality_id = self.kwargs.get('pk')
        functionality = Functionality.objects.get(id=functionality_id)
        form.instance.functionality = functionality
        form.instance.slug = slugify(form.instance.name)
        return super(FlavorCreate, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class FlavorUpdate(UpdateView):
    model = Flavor
    fields = ['name', 'slug', 'color']


@method_decorator(login_required, name='dispatch')
class FlavorDelete(DeleteView):
    model = Flavor
    success_url = reverse_lazy('home')
