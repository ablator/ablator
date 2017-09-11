from django.test import TestCase

from core.functionality import WhichContext, NoAvailability
from core.functionality.rollout_strategies import check_roll_out_recall, \
    check_roll_out_enable_globally, assert_existence_of_release
from core.models import Functionality, App, Release
from user_management.models import Organization


class RollOutRecall(TestCase):
    def test_roll_out_recall_true(self):
        context = WhichContext()
        context.functionality = Functionality(rollout_strategy=Functionality.RECALL_FUNCTIONALITY)
        with self.assertRaises(NoAvailability):
            check_roll_out_recall(context=context)

    def test_roll_out_recall_false(self):
        context = WhichContext()
        context.functionality = Functionality(rollout_strategy=Functionality.DEFINED_BY_RELEASES)
        try:
            check_roll_out_recall(context=context)
        except NoAvailability:
            self.fail()


class RollOutEnableGlobally(TestCase):
    def test_roll_out_enable_globally_true(self):
        context = WhichContext()
        context.functionality = Functionality(rollout_strategy=Functionality.ENABLE_GLOBALLY)
        availability = check_roll_out_enable_globally(context)
        self.assertIsNotNone(availability)

    def test_roll_out_enable_globally_false(self):
        context = WhichContext()
        context.functionality = Functionality(rollout_strategy=Functionality.DEFINED_BY_RELEASES)
        availability = check_roll_out_enable_globally(context)
        self.assertIsNone(availability)


class CheckExistenceOfRelease(TestCase):
    def setUp(self):
        self.organization = Organization(name='Testorganization')
        self.organization.save()
        self.app = App(name='test-app', slug='test-app', organization=self.organization)
        self.app.save()
        self.functionality = Functionality(
            app=self.app,
            name='test-func',
            slug='test-func',
        )
        self.functionality.save()

    def test_with_release_present(self):
        self.release = Release(functionality=self.functionality)
        self.release.save()
        context = WhichContext()
        context.functionality = self.functionality
        assert_existence_of_release(context)

    def test_with_release_not_present(self):
        context = WhichContext()
        context.functionality = Functionality()
        with self.assertRaises(NoAvailability):
            assert_existence_of_release(context)
