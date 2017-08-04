from django.test import TestCase

from core.functionality import *
from core.models import Functionality, Flavor


class RollOutRecall(TestCase):
    def test_roll_out_recall(self):
        context = WhichContext()
        context.functionality = Functionality(rollout_strategy=Functionality.RECALL_FEATURE)
        with self.assertRaises(NoAvailability):
            check_roll_out_recall(context=context)

    def test_roll_out_enable_globally(self):
        context = WhichContext()
        context.functionality = Functionality(rollout_strategy=Functionality.ENABLE_GLOBALLY)
        availability = check_roll_out_enable_globally(context)
        self.assertIsNotNone(availability)
