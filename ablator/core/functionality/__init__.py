from typing import Optional, List


from .availability import (
    check_for_existing_enabled_availability,
    get_availability, assert_existence_of_flavors,
    get_enabled_count,
    create_new_availability_with_random_flavor,
    enable_availability_by_user_count,
)
from .rollout_strategies import (
    check_roll_out_enable_globally,
    assert_roll_out_is_not_paused,
    assert_existence_of_release,
    check_roll_out_recall
)
from ..models import Flavor, Functionality, ClientUser, Availability


class WhichContext:
    client_user: ClientUser
    functionality: Functionality
    availability: Availability
    available_flavors: List[Flavor]
    enabled_count: int


class NoAvailability(Exception):
    pass


def can_i_use(client_user: ClientUser, functionality: Functionality) -> bool:
    """
    Is the specified user allowed to use the functionatlity?

    Returns `True` if the specified ClientUser is allowed to use the functionality group,
    `False` if the user is disallowed, or the functionality group does not exist.

    Use ClientUser.user_from_object to get or create a ClientUser instance from any hashable
    object (usually a string).
    """
    functionality = which(client_user, functionality)
    if functionality:
        return functionality.is_enabled
    return False


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

    pipeline = [
        # roll out strategies
        check_roll_out_recall,
        check_roll_out_enable_globally,

        # retrieve availability
        get_availability,

        # check availability and switch on based on max user count
        check_for_existing_enabled_availability,
        assert_roll_out_is_not_paused,
        assert_existence_of_release,
        assert_existence_of_flavors,
        get_enabled_count,
        create_new_availability_with_random_flavor,
        enable_availability_by_user_count,
    ]

    # Go through each function in the pipeline. If it yields an Availability, we're done
    # and can return it. Otherwise, continue until we hit the end, or catch a NoAvailability
    # exception.
    # Splitting the methods up like this helps with testing, caching, and gaining an overview over
    # what actually happens through logging. Hopefully.
    for func in pipeline:
        try:
            av = func(context)
            if av:
                return av
        except NoAvailability:
            return None
    return None
