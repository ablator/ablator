from typing import Optional

from .models import FunctionalityGroup, Functionality, ClientUser, Availability


def can_i_use(client_user: ClientUser, functionality_group: FunctionalityGroup) -> bool:
    """
    Is the specified user allowed to use the feature?

    Returns `True` if the specified ClientUser is allowed to use the functionality group,
    `False` if the user is disallowed, or the functionality group does not exist.

    Use ClientUser.user_from_object to get or create a ClientUser instance from any hashable
    object (usually a string).
    """
    return which(client_user, functionality_group) is not None


def which(
        client_user: ClientUser,
        functionality_group: FunctionalityGroup
) -> Optional[Functionality]:
    """
    Which Functionality of the given FunctionalityGroup is enabled for the user, if any?

    Returns a Functionality object that corresponds to the ClientUser's enabled functionality,
    or `None` if the user does not have any Functionality in the given FunctionalityGroup.

    Use ClientUser.user_from_object to get or create a ClientUser instance from any hashable
    object (usually a string).
    """
    try:
        return Availability.objects.get(
            functionality__in=functionality_group.functionality_set.all(),
            user=client_user
        ).functionality
    except Availability.DoesNotExist:
        return None
