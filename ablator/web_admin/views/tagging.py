from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from tagging.models import Tag


@method_decorator(login_required, name="dispatch")
class TagsListView(ListView):
    template_name = "tagging/list.html"

    def get_queryset(self):
        return self.request.user.ablatoruser.organization.tag_set.all()


@method_decorator(login_required, name="dispatch")
class TagCreateView(CreateView):
    model = Tag
    fields = [
        "name",
    ]

    def form_valid(self, form):
        form.instance.name = form.instance.name.lower()
        form.instance.organization = self.request.user.ablatoruser.organization
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class TagDetailView(DetailView):
    model = Tag

    def get_queryset(self):
        return self.request.user.ablatoruser.organization.tag_set.all()


@method_decorator(login_required, name="dispatch")
class TagUpdateView(UpdateView):
    model = Tag
    fields = [
        "name",
    ]

    def get_queryset(self):
        return self.request.user.ablatoruser.organization.tag_set.all()


@method_decorator(login_required, name="dispatch")
class TagDeleteView(DeleteView):
    model = Tag
    success_url = reverse_lazy("tags-list")

    def get_queryset(self):
        return self.request.user.ablatoruser.organization.tag_set.all()
