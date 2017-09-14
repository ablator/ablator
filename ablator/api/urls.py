from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^v1/caniuse/(?P<client_user_string>[^/]+)/(?P<functionality_id>[^/]+)/?$',
        views.CanIUseSingleViewV1.as_view()),
    url(r'^v1/which/(?P<client_user_string>[^/]+)/(?P<functionality_id>[^/]+)/?$',
        views.WhichSingleViewV1.as_view()),

    url(r'^v2/which/(?P<client_user_string>[^/]+)/(?P<app_id>[^/]+)/?$', views.WhichViewV2.as_view()),
    url(r'^v2/caniuse/(?P<client_user_string>[^/]+)/(?P<app_id>[^/]+)/?$', views.CanIUseViewV2.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
