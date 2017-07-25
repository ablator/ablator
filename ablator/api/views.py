from django.http.response import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from core.functionality import can_i_use
from core.models import ClientUser, Functionality


class CanIUseView(APIView):
    def get(self, request, client_user_string, functionality_id):
        functionality = get_object_or_404(Functionality, id=functionality_id)
        client_user = ClientUser.user_from_object(client_user_string)
        return Response({'enabled': can_i_use(client_user, functionality)})


class WhichView(APIView):
    def get(self, request, client_user_id, functionality_id):
        raise Http404
