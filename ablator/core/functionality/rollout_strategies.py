from django.utils import timezone
from typing import Optional, TYPE_CHECKING

from core.models import Availability, RolloutStrategy

if TYPE_CHECKING:
    from core.functionality import WhichContext


def get_rollout_strategy(context: 'WhichContext'):
    possible_rollout_strategy = context.functionality.rolloutstrategy_set.filter(
        start_at__lt=timezone.now(),
        tag__in=context.client_user.tag_set.all()
    ).order_by('priority').first()

    if not possible_rollout_strategy:
        possible_rollout_strategy = context.functionality.rolloutstrategy_set.filter(
            start_at__lt=timezone.now()
        ).order_by('priority').first()

    if not possible_rollout_strategy:
        from core.functionality import NoAvailability
        raise NoAvailability

    context.rollout_strategy = possible_rollout_strategy


def check_roll_out_recall(context: 'WhichContext'):
    if context.rollout_strategy.strategy == RolloutStrategy.RECALL_FUNCTIONALITY:
        from core.functionality import NoAvailability
        raise NoAvailability


def check_roll_out_enable_globally(context: 'WhichContext') -> Optional[Availability]:
    if context.rollout_strategy.strategy == RolloutStrategy.ENABLE_GLOBALLY:
        return Availability(
            flavor=context.rollout_strategy.possible_flavors.first(),
            is_enabled=True
        )


def assert_roll_out_is_not_paused(context: 'WhichContext'):
    """Check if Rollout is paused"""
    if context.rollout_strategy.strategy == RolloutStrategy.PAUSE_ROLLOUT:
        from core.functionality import NoAvailability
        raise NoAvailability
