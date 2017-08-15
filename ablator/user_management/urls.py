from django.conf.urls import url
from django.urls.base import reverse

from . import views

urlpatterns = [
    url(r'create/$', views.UserCreate.as_view(), name='user-create'),
    url(r'update/(?P<pk>[^/]+)/$', views.UserUpdate.as_view(), name='user-update'),
    url(r'delete/(?P<pk>[^/]+)/$', views.UserDelete.as_view(), name='user-delete'),
    url(r'$', views.UserList.as_view(), name='user-list'),
]