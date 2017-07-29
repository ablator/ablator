from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from core.functionality import can_i_use, which
from core.models import ClientUser, FunctionalityGroup


class CanIUseView(APIView):
    def get(self, request, client_user_string, functionality_group_id):
        """
        Is the specified user allowed to use the feature?

        Returns `{ "enabled": true }` if the specified ClientUser is allowed to use the
        functionality group, ``{ "enabled": false }`` if the user is disallowed, or a 404 error if
        functionality group does not exist.

        Include a string that uniquely identifies the user as the client user string.

        See also the `which` endpoint to see if a user has a specific functionality group within a
        functionality
        """
        functionality_group = get_object_or_404(FunctionalityGroup, id=functionality_group_id)
        client_user = ClientUser.user_from_object(client_user_string)
        return Response({'enabled': can_i_use(client_user, functionality_group)})


class WhichView(APIView):
    def get(self, request, client_user_string, functionality_group_id):
        """
        Which Functionality of the given FunctionalityGroup is enabled for the user, if any?

        Returns `{ "which": "<app.group.functionality>" }` that corresponds to the ClientUser's
        enabled functionality, or `{ "which": none }` if the user does not have any Functionality in
        the given FuncationlityGroup.

        If the FunctionalityGroup does not exist, this endpoint returns a 404 error.

        """
        functionality_group = get_object_or_404(FunctionalityGroup, id=functionality_group_id)
        client_user = ClientUser.user_from_object(client_user_string)
        availability = which(client_user, functionality_group)
        return Response({

            'functionality': availability.functionality.__str__() if availability else None,
            'is_enabled': availability.is_enabled if availability else False
        })
