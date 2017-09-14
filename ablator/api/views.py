from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from core.functionality import can_i_use, which
from core.models import ClientUser, Functionality, App


class CanIUseSingleViewV1(APIView):
    """
    Is the specified user allowed to use the functionality?

    Returns `{ "enabled": true }` if the specified ClientUser is allowed to use the
    functionality group, ``{ "enabled": false }`` if the user is disallowed, or a 404 error if
    functionality group does not exist.

    Include a string that uniquely identifies the user as the client user string.

    See also the `which` endpoint to see if a user has a specific functionality group within a
    functionality
    """
    def get(self, request, client_user_string, functionality_id):
        functionality = get_object_or_404(Functionality, id=functionality_id)
        client_user = ClientUser.user_from_object(client_user_string)
        return Response({'enabled': can_i_use(client_user, functionality)})


class WhichSingleViewV1(APIView):
    """
    Which Flavor of the given Functionality is enabled for the user, if any?

    Returns `{ "which": "<app.group.functionality>" }` that corresponds to the ClientUser's
    enabled functionality, or `{ "which": none }` if the user does not have any Flavor in
    the given FuncationlityGroup.

    If the Functionality does not exist, this endpoint returns a 404 error.

    """
    def get(self, request, client_user_string, functionality_id):
        functionality = get_object_or_404(Functionality, id=functionality_id)
        client_user = ClientUser.user_from_object(client_user_string)
        availability = which(client_user, functionality)
        return Response({
            'functionality': availability.flavor.__str__() if availability else None,
        })


class WhichViewV2(APIView):
    """
    Returns a list of all availabilities that are enabled for the given user
    in the given app.

    Availabilities that are not enabled are not listed.

    Returns a list of strings, which correspond to the fqdn strings of the enabled flavors.
    Example:

        [
            "masa.rover.atmospheric-regulator.power-save-mode",
            "masa.rover.dehumidifier.dry-as-bone"
        ]
    """
    def get(self, request, client_user_string, app_id):
        app = get_object_or_404(App, id=app_id)
        client_user = ClientUser.user_from_object(client_user_string)
        availabilities = [
            which(client_user, functionality)
            for functionality in app.functionality_set.all()
        ]
        return Response([
            availability.flavor.__str__()
            for availability in availabilities
            if availability
        ])


class CanIUseViewV2(APIView):
    """
    Returns a list of enabled functionalities of the specified app.

    Functionalities that are not enabled are not shown.

    This is the preferred endpoint to use if you are using ablator only as an on/off switch for
    features. To get to a list of flavors instead, use the `which` endpoint.

    Returns a list of strings, which correspond to the fqdn strings of the enabled
    functionalities. Example:

        [
            "masa.rover.atmospheric-regulator",
            "masa.rover.space-heater"
        ]
    """
    def get(self, request, client_user_string, app_id):
        app = get_object_or_404(App, id=app_id)
        client_user = ClientUser.user_from_object(client_user_string)
        functionalities = [
            functionality
            for functionality in app.functionality_set.all()
            if can_i_use(client_user, functionality)
        ]
        return Response([
            functionality.__str__()
            for functionality in functionalities
        ])
