from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import Organization, AblatorUser


class OrganizationField(forms.CharField):
    def validate(self, value):
        super().validate(value)
        try:
            Organization.objects.get(slug=slugify(value))
            raise ValidationError('An organization with this name already exists. If you are a '
                                  'member of this organization, ask your administrator to '
                                  'invite you.')
        except Organization.DoesNotExist:
            pass


class OrganizationRegisterForm(forms.Form):
    organization_name = OrganizationField(max_length=140)
    user_name = forms.CharField(max_length=140)
    user_email = forms.EmailField()
    user_password = forms.CharField(widget=forms.PasswordInput())

    def create_organization(self):
        new_organization = Organization.objects.create(
            name=self.cleaned_data['organization_name'],
            slug=slugify(self.cleaned_data['organization_name']),

        )
        new_user = User.objects.create_user(
            self.cleaned_data['user_name'],
            self.cleaned_data['user_email'],
            self.cleaned_data['user_password']
        )
        new_user.is_staff = True

        new_ablator_user = AblatorUser.objects.create(
            user=new_user,
            organization=new_organization
        )

        return new_ablator_user
