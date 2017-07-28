import random
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


def which(client_user: ClientUser, functionality_group: FunctionalityGroup) -> Optional[Functionality]:
    """
    Which Functionality of the given FunctionalityGroup is enabled for the user, if any?

    Returns a Functionality object that corresponds to the ClientUser's enabled functionality,
    or `None` if the user does not have any Functionality in the given FunctionalityGroup.

    Use ClientUser.user_from_object to get or create a ClientUser instance from any hashable
    object (usually a string).
    """
    # TODO: Split up this function

    # Check Roll Out Strategy
    if functionality_group.rollout_strategy == FunctionalityGroup.RECALL_FEATURE:
        return None

    if functionality_group.rollout_strategy == FunctionalityGroup.ENABLE_GLOBALLY:
        return FunctionalityGroup.functionality_set.first()

    # Retrieve Functionality Instance
    try:
        availability = Availability.objects.select_related('functionality').get(
            functionality__in=functionality_group.functionality_set.all(),
            user=client_user
        )
    except Availability.DoesNotExist:
        availability = None

    # Easiest Case: Already enabled
    if availability and availability.is_enabled:
        return availability.functionality

    # Already Exists, but disabled
    if availability and not availability.is_enabled:
        if functionality_group.rollout_strategy == FunctionalityGroup.PAUSE_ROLLOUT:
            return availability.functionality
        elif functionality_group.rollout_strategy == FunctionalityGroup.DEFINED_BY_RELEASES:
            enabled_count = Availability.objects.filter(
                functionality__group=functionality_group,
                is_enabled=True
            ).count()
            if functionality_group.current_release.max_enabled_users > enabled_count:
                availability.is_enabled = True
                availability.save()
            return availability

    # Check if Rollout is paused
    if functionality_group.rollout_strategy == FunctionalityGroup.PAUSE_ROLLOUT:
        return None

    # Availability does not yet exist. Choose a Functionality at random
    if not functionality_group.current_release:
        return None

    functionalities = functionality_group.functionality_set.all()
    if functionalities:
        availability = Availability()
        availability.user = client_user
        availability.functionality = functionalities[random.randint(0, len(functionalities))-1]

    enabled_count = Availability.objects.filter(
        functionality__group=functionality_group,
        is_enabled=True
    ).count()
    availability.is_enabled = (functionality_group.current_release.max_enabled_users > enabled_count)
    return availability.functionality
