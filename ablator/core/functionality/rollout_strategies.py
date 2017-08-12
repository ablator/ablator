from typing import Optional

from core.models import Functionality, Availability


def check_roll_out_recall(context: 'WhichContext'):
    if context.functionality.rollout_strategy == Functionality.RECALL_FUNCTIONALITY:
        from core.functionality import NoAvailability
        raise NoAvailability


def check_roll_out_enable_globally(context: 'WhichContext') -> Optional[Availability]:
    if context.functionality.rollout_strategy == Functionality.ENABLE_GLOBALLY:
        return Availability(
            flavor=context.functionality.flavor_set.first(),
            is_enabled=True
        )


def assert_roll_out_is_not_paused(context: 'WhichContext'):
    """Check if Rollout is paused"""
    if context.functionality.rollout_strategy == Functionality.PAUSE_ROLLOUT:
        from core.functionality import NoAvailability
        raise NoAvailability


def assert_existence_of_release(context: 'WhichContext'):
    if not context.functionality.current_release:
        from core.functionality import NoAvailability
        raise NoAvailability
