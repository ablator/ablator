from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import app, functionality, index
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Accounts
    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(), name='logout'),

    # Apps
    url(r'app/create/$', app.AppCreate.as_view(), name='app-create'),
    url(r'^app/(?P<app_id>[^/]+)/$', app.AppDetail.as_view(), name='app-detail'),
    url(r'app/(?P<pk>[^/]+)/update/$', app.AppUpdate.as_view(), name='app-update'),
    url(r'app/(?P<pk>[^/]+)/delete/$', app.AppDelete.as_view(), name='app-delete'),

    # Functionality
    url(r'^functionality/(?P<functionality_id>[^/]+)/$', functionality.FunctionalityDetail.as_view(), name='functionality'),

    # Home Page
    url('$', index.HomePageView.as_view(), name='home'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
