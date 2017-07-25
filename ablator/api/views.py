from django.http.response import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from core.functionality import can_i_use, which
from core.models import ClientUser, Functionality, FunctionalityGroup


class CanIUseView(APIView):
    def get(self, request, client_user_string, functionality_group_id):
        functionality_group = get_object_or_404(FunctionalityGroup, id=functionality_group_id)
        client_user = ClientUser.user_from_object(client_user_string)
        return Response({'enabled': can_i_use(client_user, functionality_group)})


class WhichView(APIView):
    def get(self, request, client_user_string, functionality_group_id):
        functionality_group = get_object_or_404(FunctionalityGroup, id=functionality_group_id)
        client_user = ClientUser.user_from_object(client_user_string)
        functionality = which(client_user, functionality_group)
        return Response({'which': functionality.__str__() if functionality else None})
