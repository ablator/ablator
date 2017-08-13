import random
from typing import Optional

from core.models import Availability, Functionality


def _availability_or_none(availability):
    if availability:
        if availability.is_enabled:
            return availability
    return None


def get_availability(context: 'WhichContext'):
    try:
        context.availability = Availability.objects.select_related('flavor').get(
            flavor__in=context.functionality.flavor_set.all(),
            user=context.client_user
        )
    except Availability.DoesNotExist:
        context.availability = None


def check_for_existing_enabled_availability(context: 'WhichContext') -> Optional['Availability']:
    return _availability_or_none(context.availability)


def get_enabled_count(context: 'WhichContext'):
    context.enabled_count = Availability.objects.filter(
        flavor__functionality=context.functionality,
        is_enabled=True
    ).count()


def enable_availability_by_user_count(context: 'WhichContext') -> Optional['Availability']:
    """
    Availability already exists, but is disabled, so enable if there are still user slots left in
    max_enabled_users
    """
    if context.functionality.rollout_strategy == Functionality.DEFINED_BY_RELEASES:
        if context.availability.is_enabled:
            return context.availability
        if context.functionality.current_release.max_enabled_users > context.enabled_count:
            context.availability.is_enabled = True
            context.availability.save()
            return _availability_or_none(context.availability)
        from ..functionality import NoAvailability
        raise NoAvailability


def assert_existence_of_flavors(context: 'WhichContext'):
    context.available_flavors = context.functionality.flavor_set.all()
    if context.available_flavors:
        return None
    from core.functionality import NoAvailability
    raise NoAvailability


def create_new_availability_with_random_flavor(context: 'WhichContext'):
    if not context.availability:
        availability = Availability()
        availability.user = context.client_user
        availability.flavor = random.choice(context.available_flavors)
        availability.save()
        context.availability = availability
