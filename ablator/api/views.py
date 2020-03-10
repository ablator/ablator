import json

from django.utils.text import slugify
from rest_framework.generics import get_object_or_404, ListAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.functionality import can_i_use, which
from core.models import ClientUser, Functionality, App
from tagging.models import Tag
from tagging.serializers import TagSerializer
from telemetry.models import Signal, SignalType
from telemetry.serializers import SignalTypeSerializer, SignalSerializer


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
        client_user = ClientUser.user_from_object(client_user_string, organization=functionality.app.organization)
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
        client_user = ClientUser.user_from_object(client_user_string, organization=functionality.app.organization)
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
    def get(self, request, organization_id, client_user_string, app_id):
        app = get_object_or_404(App, id=app_id)
        client_user = ClientUser.user_from_object(client_user_string, app.organization)
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
    def get(self, request, organization_id, client_user_string, app_id):
        app = get_object_or_404(App, id=app_id)
        client_user = ClientUser.user_from_object(client_user_string, organization=app.organization)
        functionalities = [
            functionality
            for functionality in app.functionality_set.all()
            if can_i_use(client_user, functionality)
        ]
        return Response([
            functionality.__str__()
            for functionality in functionalities
        ])


class CanIUseViewV4(APIView):
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
        client_user = ClientUser.user_from_object(client_user_string, organization=app.organization)
        functionalities = [
            functionality
            for functionality in app.functionality_set.all()
            if can_i_use(client_user, functionality)
        ]
        return Response([
            functionality.__str__()
            for functionality in functionalities
        ])


class TagListViewV3(ListAPIView):
    """
    Returns a list of all Tags applied to the specified User within the specified Organization.

    Tags that are present in the Organization but not applied to the User are not shown.

    Note that even though this API endpoint takes an App ID as its parameter, Tags are available
    to a complete Organization, meaning that if an Organization has multiple Apps, the Tags are shared
    between those apps. If you'd like App-specific Tags, you can prefix them with the app's name or
    something similar.

    To remove a User's associated Tag, use `/api/v3/<user>/<organization_id>/tag/<tag_name>/remove`
    """
    serializer_class = TagSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        client_user_string = self.kwargs['client_user_string']
        user = ClientUser.user_from_object(client_user_string, organization=self.kwargs['organization_id'])
        return user.tag_set.all()

    def post(self, request, organization_id, client_user_string, app_id):
        app = App.objects.get(id=app_id)
        user = ClientUser.user_from_object(client_user_string, organization_id=organization_id)
        newTag = Tag.objects.get_or_create(
            name=slugify(request.data['name']),
            organization=app.organization
        )[0]
        newTag.users.add(user)
        newTag.save()

        return self.get(request, client_user_string, app_id)


class TagRemoveViewV3(DestroyAPIView):
    """
    Removes the association between a specified User and Tag.

    The Tag object itself is not deleted.

    Note that because Tags are shared between all Apps of an Organization, the other Apps under the
    same Organization will also lose the association between User and Tag. If you'd like App-specific
    Tags, you can prefix them with the app's name or something similar.
    """
    permission_classes = [AllowAny, ]

    def delete(self, request, organization_id, client_user_string, app_id, tag_name):
        client_user_string = self.kwargs['client_user_string']
        user = ClientUser.user_from_object(client_user_string, organization_id=organization_id)
        tag = get_object_or_404(user.tag_set.all(), name=tag_name)
        user.tag_set.remove(tag)


class PostSignalViewV4(APIView):
    def post(self, request, client_user_string, app_id, signal_name):
        app = App.objects.get(id=app_id)
        user = ClientUser.user_from_object(client_user_string, organization_id=app.organization_id)
        signal_type = SignalType.objects.get_or_create(name=slugify(signal_name), app=app)[0]

        new_signal = Signal(parameters=json.dumps(request.data))
        new_signal.user = user
        new_signal.type = signal_type
        new_signal.save()

        return self.get(request, client_user_string, app_id, signal_name)
