from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from web_admin.views import HomePageView
from . import views

urlpatterns = [
    url('$', HomePageView.as_view(), name='home')
]

urlpatterns = format_suffix_patterns(urlpatterns)
