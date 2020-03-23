from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView

from .forms import OrganizationRegisterForm
from .models import AblatorUser, Organization


class OrganizationRegisterView(FormView):
    template_name = "user_management/register.html"
    form_class = OrganizationRegisterForm
    success_url = "/"

    def form_valid(self, form: OrganizationRegisterForm):
        new_ablator_user = form.create_organization()
        message = (
            '<h4 class="alert-heading">Registration Complete!</h4>'
            "Your new organization, <b>{}</b>, was created successful. User <b>{}</b> is the "
            "administrator of this organization. <hr>"
            "You can now log in below with your new user credentials."
        )
        message = message.format(new_ablator_user.organization, new_ablator_user)
        messages.success(self.request, message)
        return super().form_valid(form)


@method_decorator(staff_member_required(login_url="login"), name="dispatch")
class UserList(ListView):
    model = User

    def get_queryset(self):
        return User.objects.filter(ablatoruser__organization=self.request.user.ablatoruser.organization)


@method_decorator(staff_member_required(login_url="login"), name="dispatch")
class UserCreate(CreateView):
    model = User
    fields = ["username", "first_name", "last_name", "email", "is_staff"]
    success_url = reverse_lazy("user-list")

    def form_valid(self, form):
        form.instance.save()
        ablatoruser = AblatorUser(user=form.instance, organization=self.request.user.ablatoruser.organization)
        ablatoruser.save()
        form.instance.ablatoruser = ablatoruser
        return super().form_valid(form)


@method_decorator(staff_member_required(login_url="login"), name="dispatch")
class UserUpdate(UpdateView):
    model = User
    fields = ["username", "first_name", "last_name", "email", "is_staff"]
    success_url = reverse_lazy("user-list")

    def get_queryset(self):
        return User.objects.filter(ablatoruser__organization=self.request.user.ablatoruser.organization)


@method_decorator(staff_member_required(login_url="login"), name="dispatch")
class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy("user-list")

    def get_queryset(self):
        return User.objects.filter(ablatoruser__organization=self.request.user.ablatoruser.organization)


@method_decorator(staff_member_required(login_url="login"), name="dispatch")
class OrganizationUpdate(UpdateView):
    model = Organization
    success_url = reverse_lazy("user-list")
    fields = ["name", "slug"]

    def get_queryset(self):
        return Organization.objects.filter(id=self.request.user.ablatoruser.organization.id)


@method_decorator(login_required, name="dispatch")
class UserDetail(DetailView):
    model = User

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


@method_decorator(login_required, name="dispatch")
class UserPasswordUpdateView(FormView):
    template_name = "user_management/change_password.html"

    def get_form(self, form_class=None):
        user = self.request.user
        form = PasswordChangeForm(user=user, **self.get_form_kwargs())
        return form

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        message = "Your password has been successfully changed."
        messages.success(self.request, message)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("profile-detail", kwargs={"pk": self.kwargs["pk"]})
