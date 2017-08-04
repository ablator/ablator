import random
from typing import Optional

from .availability_or_none import _availability_or_none
from ..models import Functionality, ClientUser, Availability


def can_i_use(client_user: ClientUser, functionality: Functionality) -> bool:
    """
    Is the specified user allowed to use the feature?

    Returns `True` if the specified ClientUser is allowed to use the functionality group,
    `False` if the user is disallowed, or the functionality group does not exist.

    Use ClientUser.user_from_object to get or create a ClientUser instance from any hashable
    object (usually a string).
    """
    functionality = which(client_user, functionality)
    if functionality:
        return functionality.is_enabled
    return False


class WhichContext:
    client_user: ClientUser
    functionality: Functionality


class NoAvailability(Exception):
    pass


def check_roll_out_recall(context: WhichContext):
    if context.functionality.rollout_strategy == Functionality.RECALL_FEATURE:
        raise NoAvailability


def check_roll_out_enable_globally(context: WhichContext) -> Optional[Availability]:
    if context.functionality.rollout_strategy == Functionality.ENABLE_GLOBALLY:
        return Availability(
            flavor=context.functionality.flavor_set.first(),
            is_enabled=True
        )


def which(client_user: ClientUser, functionality: Functionality) -> Optional[Availability]:
    """
    Which Flavor of the given Functionality is enabled for the user, if any?

    Returns a Flavor object that corresponds to the ClientUser's enabled functionality,
    or `None` if the user does not have any Flavor in the given Functionality.

    Use ClientUser.user_from_object to get or create a ClientUser instance from any hashable
    object (usually a string).
    """
    context = WhichContext()
    context.client_user = client_user
    context.functionality = functionality

    checking_pipeline = [
        check_roll_out_recall,
        check_roll_out_enable_globally,
    ]

    # Go through each function in the checking pipeline. If it yields an Availability, we're done
    # and can return it. Otherwise, continue until we hit the end, or catch a NoAvailability
    # exception.
    # Splitting the methods up like this helps with testing, caching, and gaining an overview over
    # what actually happens. Hopefully.
    for func in checking_pipeline:
        try:
            availability = func(context)
            if availability:
                return availability
        except NoAvailability:
            return None
    return None




    # Retrieve Availability and Flavor Instances
    try:
        availability = Availability.objects.select_related('flavor').get(
            flavor__in=functionality.flavor_set.all(),
            user=client_user
        )
    except Availability.DoesNotExist:
        availability = None

    # Easiest Case: Already enabled
    if availability and availability.is_enabled:
        return availability

    # Already Exists, but disabled
    if availability and not availability.is_enabled:
        if functionality.rollout_strategy == Functionality.PAUSE_ROLLOUT:
            return availability.functionality
        elif functionality.rollout_strategy == Functionality.DEFINED_BY_RELEASES:
            enabled_count = Availability.objects.filter(
                flavor__functionality=functionality,
                is_enabled=True
            ).count()
            if functionality.current_release.max_enabled_users > enabled_count:
                availability.is_enabled = True
                availability.save()
            return _availability_or_none(availability)

    # Check if Rollout is paused
    if functionality.rollout_strategy == Functionality.PAUSE_ROLLOUT:
        return None

    # Availability does not yet exist. Choose a Flavor at random
    if not functionality.current_release:
        return None

    flavors = functionality.flavor_set.all()
    if flavors:
        availability = Availability()
        availability.user = client_user
        availability.flavor = random.choice(flavors)

        enabled_count = Availability.objects.filter(
            flavor__functionality=functionality,
            is_enabled=True
        ).count()
        availability.is_enabled = (
            functionality.current_release.max_enabled_users > enabled_count
        )
        availability.save()
    return _availability_or_none(availability)
