from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^app/(?P<app_id>[^/]+)/$', views.AppView.as_view(), name='app'),
    url(r'^functionality/(?P<functionality_id>[^/]+)/$', views.FunctionalityView.as_view(), name='functionality'),
    url('$', views.HomePageView.as_view(), name='home'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
