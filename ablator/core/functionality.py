from typing import Optional

from .models import Functionality, ClientUser


def can_i_use(client_user: ClientUser, functionality: Functionality) -> bool:
    return which(client_user, functionality) is not None


def which(client_user: ClientUser, functionality: Functionality) -> Optional[Functionality]:
    return None
