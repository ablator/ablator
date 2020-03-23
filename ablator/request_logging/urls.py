from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

# flake8: noqa: E501

urlpatterns = [
    url(r"(?P<pk>[^/]+)/$", LogList.as_view(), name="logging-list"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
