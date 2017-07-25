from django.http.response import Http404
from rest_framework.views import APIView


class CanIUseView(APIView):
    def get(self, request, client_user_id, feature_id):
        raise Http404


class WhichView(APIView):
    def get(self, request, client_user_id, feature_id):
        raise Http404
