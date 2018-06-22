from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import app, functionality, index, flavor, release, availability
from django.contrib.auth import views as auth_views

# flake8: noqa: E501

urlpatterns = [
    # Account
    url(r'accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'accounts/logout/$', auth_views.LogoutView.as_view(), name='logout'),

    # App
    url(r'app/create/$', app.AppCreate.as_view(), name='app-create'),
    url(r'app/(?P<app_id>[^/]+)/$', app.AppDetail.as_view(), name='app-detail'),
    url(r'app/(?P<pk>[^/]+)/update/$', app.AppUpdate.as_view(), name='app-update'),
    url(r'app/(?P<pk>[^/]+)/delete/$', app.AppDelete.as_view(), name='app-delete'),

    # Functionality
    url(r'app/(?P<pk>[^/]+)/add_functionality/$', functionality.FunctionalityCreate.as_view(), name='functionality-create'),
    url(r'functionality/(?P<pk>[^/]+)/$', functionality.FunctionalityDetail.as_view(), name='functionality-detail'),
    url(r'functionality/(?P<pk>[^/]+)/update/$', functionality.FunctionalityUpdate.as_view(), name='functionality-update'),
    url(r'functionality/(?P<pk>[^/]+)/delete/$', functionality.FunctionalityDelete.as_view(), name='functionality-delete'),

    # Functionality Partials
    url(r'functionality/enabled-users/(?P<pk>[^/]+)/$', functionality.FunctionalityPartEnabledUsers.as_view(), name='functionality-part-enabled-users'),
    url(r'functionality/progress/(?P<pk>[^/]+)/$', functionality.FunctionalityPartProgress.as_view(), name='functionality-part-progress'),
    url(r'functionality/flavors/(?P<pk>[^/]+)/$', functionality.FunctionalityPartFlavors.as_view(), name='functionality-part-flavors'),

    # Flavor
    url(r'functionality/(?P<pk>[^/]+)/add_flavor/$', flavor.FlavorCreate.as_view(), name='flavor-create'),
    url(r'flavor/(?P<pk>[^/]+)/update/$', flavor.FlavorUpdate.as_view(), name='flavor-update'),
    url(r'flavor/(?P<pk>[^/]+)/delete/$', flavor.FlavorDelete.as_view(), name='flavor-delete'),

    # Release
    url(r'functionality/(?P<pk>[^/]+)/add_release/$', release.ReleaseCreate.as_view(), name='release-create'),
    url(r'release/(?P<pk>[^/]+)/update/$', release.ReleaseUpdate.as_view(), name='release-update'),
    url(r'release/(?P<pk>[^/]+)/delete/$', release.ReleaseDelete.as_view(), name='release-delete'),

    # Home Page
    url(r'^$', index.HomePageView.as_view(), name='home'),
    url(r'^status/?$', index.StatusView.as_view(), name='status'),

    # User Profiling
    url(r'availability/$', availability.AvailabilitySearch.as_view(), name='availability-index'),
    url(r'availability/(?P<user>[^/]+)/$', availability.AvailabilityList.as_view(), name='availability-list'),
    url(r'availability/(?P<user>[^/]+)/(?P<pk>[^/]+)/update/$', availability.AvailabilityUpdate.as_view(), name='availability-update'),
    url(r'availability/(?P<user>[^/]+)/(?P<pk>[^/]+)/delete/$', availability.AvailabilityDelete.as_view(), name='availability-delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
