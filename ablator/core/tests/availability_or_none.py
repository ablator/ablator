from django.test import TestCase

from core.functionality import _availability_or_none
from core.models import Availability


class AvailabilityOrNone(TestCase):
    def test_none(self):
        self.assertIsNone(_availability_or_none(None))

    def test_not_enabled(self):
        self.assertIsNone(_availability_or_none(Availability(is_enabled=False)))

    def test_enabled(self):
        availability = Availability(is_enabled=True)
        self.assertEqual(_availability_or_none(availability), availability)