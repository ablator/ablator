from unittest import mock

from django.test import TestCase

from core.functionality import can_i_use
from core.models import ClientUser, Functionality, Availability


class CanIUse(TestCase):
    @mock.patch('core.functionality.which', return_value=None)
    def test_none(self, which):
        self.assertFalse(
            can_i_use(
                ClientUser.user_from_object('test'),
                functionality=Functionality()
            )
        )

    @mock.patch('core.functionality.which', return_value=Availability(is_enabled=False))
    def test_not_enabled(self, which):
        self.assertFalse(
            can_i_use(
                ClientUser.user_from_object('test'),
                functionality=Functionality()
            )
        )

    @mock.patch('core.functionality.which', return_value=Availability(is_enabled=True))
    def test_enabled(self, which):
        self.assertTrue(
            can_i_use(
                ClientUser.user_from_object('test'),
                functionality=Functionality()
            )
        )