from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# flake8: noqa


# v1 API
urlpatternsV1 = [
    url(r'^v1/caniuse/(?P<client_user_string>[^/]+)/(?P<functionality_id>[^/]+)/?$', views.CanIUseSingleViewV1.as_view()),
    url(r'^v1/which/(?P<client_user_string>[^/]+)/(?P<functionality_id>[^/]+)/?$', views.WhichSingleViewV1.as_view()),
]

# v2 API
urlpatternsV2 = [
    url(r'^v2/which/(?P<client_user_string>[^/]+)/(?P<app_id>[^/]+)/?$', views.WhichViewV2.as_view()),
    url(r'^v2/caniuse/(?P<client_user_string>[^/]+)/(?P<app_id>[^/]+)/?$', views.CanIUseViewV2.as_view()),
]

# v3 API
urlpatternsV3 = [
    url(r'^v3/(?P<organization_id>[^/]+)/(?P<client_user_string>[^/]+)/(?P<app_id>[^/]+)/caniuse/?$', views.CanIUseViewV2.as_view()),
    url(r'^v3/(?P<organization_id>[^/]+)/(?P<client_user_string>[^/]+)/(?P<app_id>[^/]+)/flavors/?$', views.WhichViewV2.as_view()),
    url(r'^v3/(?P<organization_id>[^/]+)/(?P<client_user_string>[^/]+)/(?P<app_id>[^/]+)/tag/?$', views.TagListViewV3.as_view()),
    url(r'^v3/(?P<organization_id>[^/]+)/(?P<client_user_string>[^/]+)/(?P<app_id>[^/]+)/tag/(?P<tag_name>[^/]+)/remove/?$', views.TagRemoveViewV3.as_view()),
]

# Complete API
urlpatterns = format_suffix_patterns(urlpatternsV1 + urlpatternsV2 + urlpatternsV3)
