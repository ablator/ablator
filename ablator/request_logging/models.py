from typing import Optional
from datetime import datetime

from core.models import Functionality, Flavor


class RequestLog:
    _functionality: Optional[Functionality] = None
    _flavor: Optional[Flavor] = None

    def __init__(self, functionality_id: str, flavor_id: Optional[str],
                 timestamp: datetime, action: str, client_user_id: str = None,
                 elapsed_time: float = None):
        self.functionality_id = functionality_id
        self.flavor_id = flavor_id
        self.timestamp = timestamp
        self.action = action
        self.client_user_id = client_user_id
        self.elapsed_time = elapsed_time

    @property
    def functionality(self):
        if self._functionality:
            return self._functionality

        if self.functionality_id:
            self._functionality = Functionality.objects.get(id=self.functionality_id)
            return self._functionality

    @property
    def flavor(self):
        if self._flavor:
            return self._flavor

        if self.flavor_id:
            self._flavor = Flavor.objects.get(id=self.flavor_id)
            return self._flavor

    @property
    def client_user_id_short(self):
        return str(self.client_user_id)[:6]
