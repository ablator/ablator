from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from core.models import Release, Functionality


@method_decorator(login_required, name='dispatch')
class ReleaseCreate(CreateView):
    model = Release
    fields = ['start_at', 'max_enabled_users']

    def form_valid(self, form):
        functionality_id = self.kwargs.get('pk')
        functionality = Functionality.objects.get(id=functionality_id)
        form.instance.functionality = functionality
        return super(ReleaseCreate, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class ReleaseUpdate(UpdateView):
    model = Release
    fields = ['start_at', 'max_enabled_users']


@method_decorator(login_required, name='dispatch')
class ReleaseDelete(DeleteView):
    model = Release
    success_url = reverse_lazy('home')
