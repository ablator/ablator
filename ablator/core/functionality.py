from typing import Optional

from core.models import FunctionalityGroup, Functionality, ClientUser, Availability


def can_i_use(client_user: ClientUser, functionality_group: FunctionalityGroup) -> bool:
    return which(client_user, functionality_group) is not None


def which(client_user: ClientUser, functionality_group: FunctionalityGroup) -> Optional[Functionality]:
    try:
        return Availability.objects.get(
            functionality__in=functionality_group.functionality_set.all(),
            user=client_user
        ).functionality
    except Availability.DoesNotExist:
        return None
