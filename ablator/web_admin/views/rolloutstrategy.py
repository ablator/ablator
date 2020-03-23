from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from core.models import RolloutStrategy, Functionality
from web_admin.forms.RolloutStrategyForm import RolloutStrategyForm


@method_decorator(login_required, name="dispatch")
class RolloutStrategyCreate(CreateView):
    template_name = "core/rolloutstrategy_form.html"

    def get_initial(self):
        initial = super(RolloutStrategyCreate, self).get_initial()

        functionality_id = self.kwargs.get("pk")
        functionality = Functionality.objects.get(id=functionality_id)
        initial["functionality"] = functionality
        return initial

    def get_form(self, form_class=None):
        functionality_id = self.kwargs.get("pk")
        functionality = Functionality.objects.get(id=functionality_id)

        if form_class is None:
            form_class = RolloutStrategyForm
        return form_class(functionality, **self.get_form_kwargs())

    def form_valid(self, form):
        # Always set the functionality from the URL
        functionality_id = self.kwargs.get("pk")
        functionality = Functionality.objects.get(id=functionality_id)
        form.instance.functionality = functionality

        return super(RolloutStrategyCreate, self).form_valid(form)


@method_decorator(login_required, name="dispatch")
class RolloutStrategyUpdate(UpdateView):
    form_class = RolloutStrategyForm
    template_name = "core/rolloutstrategy_form.html"

    def get_form(self, form_class=None):
        rollout_strategy_id = self.kwargs.get("pk")
        rollout_strategy = RolloutStrategy.objects.get(id=rollout_strategy_id)
        functionality = rollout_strategy.functionality

        if form_class is None:
            form_class = RolloutStrategyForm
        return form_class(functionality, **self.get_form_kwargs())

    def get_queryset(self):
        return RolloutStrategy.objects.all()


@method_decorator(login_required, name="dispatch")
class RolloutStrategyDelete(DeleteView):
    model = RolloutStrategy
    success_url = reverse_lazy("home")
