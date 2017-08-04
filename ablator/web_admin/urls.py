from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    url('$', views.HomePageView.as_view(), name='home'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
