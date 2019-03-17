from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import app, functionality, index, flavor, rolloutstrategy, availability, tagging
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

    # Rollout Strategy
    url(r'functionality/(?P<pk>[^/]+)/add_rolloutstrategy/$', rolloutstrategy.RolloutStrategyCreate.as_view(), name='rollout-strategy-create'),
    url(r'rolloutstrategy/(?P<pk>[^/]+)/update/$', rolloutstrategy.RolloutStrategyUpdate.as_view(), name='rollout-strategy-update'),
    url(r'rolloutstrategy/(?P<pk>[^/]+)/delete/$', rolloutstrategy.RolloutStrategyDelete.as_view(), name='rollout-strategy-delete'),

    # Home Page
    url(r'^$', index.HomePageView.as_view(), name='home'),
    url(r'^status/?$', index.StatusView.as_view(), name='status'),

    # User Profiling
    url(r'availability/$', availability.AvailabilitySearch.as_view(), name='availability-index'),
    url(r'availability/(?P<user>[^/]+)/$', availability.AvailabilityList.as_view(), name='availability-list'),
    url(r'availability/(?P<user>[^/]+)/(?P<pk>[^/]+)/update/$', availability.AvailabilityUpdate.as_view(), name='availability-update'),
    url(r'availability/(?P<user>[^/]+)/(?P<pk>[^/]+)/delete/$', availability.AvailabilityDelete.as_view(), name='availability-delete'),

    # Tags
    url(r'tags/$', tagging.TagsListView.as_view(), name='tags-list'),
    url(r'tags/create/$', tagging.TagCreateView.as_view(), name='tags-create'),
    url(r'tags/(?P<pk>[^/]+)/$', tagging.TagDetailView.as_view(), name='tags-detail'),
    url(r'tags/(?P<pk>[^/]+)/update/$', tagging.TagUpdateView.as_view(), name='tags-update'),
    url(r'tags/(?P<pk>[^/]+)/delete/$', tagging.TagDeleteView.as_view(), name='tags-delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
