from django.test import TestCase
from unittest import mock

from core.functionality import _availability_or_none
from core.models import ClientUser, Functionality, Flavor, Availability
from .functionality import can_i_use, which


def mocked_which(*args, **kwargs):
    return None


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


class AvailabilityOrNone(TestCase):
    def test_none(self):
        self.assertIsNone(_availability_or_none(None))

    def test_not_enabled(self):
        self.assertIsNone(_availability_or_none(Availability(is_enabled=False)))

    def test_enabled(self):
        availability = Availability(is_enabled=True)
        self.assertEqual(_availability_or_none(availability), availability)