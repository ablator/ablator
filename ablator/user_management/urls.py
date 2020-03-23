from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"organization/register/$", views.OrganizationRegisterView.as_view(), name="organization-register"),
    url(r"users/create/$", views.UserCreate.as_view(), name="user-create"),
    url(r"users/update/(?P<pk>[^/]+)/$", views.UserUpdate.as_view(), name="user-update"),
    url(r"users/delete/(?P<pk>[^/]+)/$", views.UserDelete.as_view(), name="user-delete"),
    url(r"users/change_password/$", views.UserPasswordUpdateView.as_view(), name="user-password-change"),
    url(r"organization/update/(?P<pk>[^/]+)/$", views.OrganizationUpdate.as_view(), name="organization-update"),
    url(r"profile/(?P<pk>[^/]+)/$", views.UserDetail.as_view(), name="profile-detail"),
    url(r"$", views.UserList.as_view(), name="user-list"),
]
