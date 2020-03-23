from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView, UpdateView, DeleteView

from core.models import Availability, ClientUser
from web_admin.forms.AvailabilitySearchForm import SearchForm


@method_decorator(login_required, name="dispatch")
class AvailabilitySearch(FormView):
    template_name = "core/availability/search.html"
    form_class = SearchForm

    def form_valid(self, form):
        user_key = form.cleaned_data["user_identity_string"]
        return HttpResponseRedirect(reverse_lazy("availability-list", kwargs={"user": user_key}))


@method_decorator(login_required, name="dispatch")
class AvailabilityList(ListView):
    template_name = "core/availability/list.html"

    def get_queryset(self):
        client_user = ClientUser.user_from_object(self.kwargs["user"], organization=self.request.user.ablatoruser.organization)
        return Availability.objects.filter(flavor__functionality__app__organization=self.request.user.ablatoruser.organization).filter(
            user=client_user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_identifier"] = self.kwargs["user"]
        return context


@method_decorator(login_required, name="dispatch")
class AvailabilityUpdate(UpdateView):
    template_name = "core/availability/update.html"
    fields = [
        "flavor",
        "is_enabled",
    ]

    def get_success_url(self):
        return reverse_lazy("availability-list", kwargs={"user": self.kwargs["user"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_identifier"] = self.kwargs["user"]
        return context

    def get_queryset(self):
        return Availability.objects.filter(flavor__functionality__app__organization=self.request.user.ablatoruser.organization)


@method_decorator(login_required, name="dispatch")
class AvailabilityDelete(DeleteView):
    template_name = "core/availability/confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("availability-list", kwargs={"user": self.kwargs["user"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_identifier"] = self.kwargs["user"]
        return context

    def get_queryset(self):
        return Availability.objects.filter(flavor__functionality__app__organization=self.request.user.ablatoruser.organization)
