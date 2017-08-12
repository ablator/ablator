from django.test import TestCase

from core.functionality import WhichContext
from core.functionality.availability import check_for_existing_enabled_availability, \
    get_availability, \
    enable_or_create_availability_by_user_count, _availability_or_none, \
    assert_existence_of_flavors
from core.models import Availability, ClientUser, Functionality, App, Flavor, Release


class AvailabilityOrNone(TestCase):
    def test_none(self):
        self.assertIsNone(_availability_or_none(None))

    def test_not_enabled(self):
        self.assertIsNone(_availability_or_none(Availability(is_enabled=False)))

    def test_enabled(self):
        availability = Availability(is_enabled=True)
        self.assertEqual(_availability_or_none(availability), availability)


class GetAvailability(TestCase):
    def setUp(self):
        self.user = ClientUser.user_from_object('testuser')
        self.user.save()
        app = App(name='Test App', slug='test-app')
        app.save()
        self.functionality = Functionality(app=app, name='Test Func', slug='test-func')
        self.functionality.save()
        flavor = Flavor(name='Flav', slug='flav', functionality=self.functionality)
        flavor.save()
        self.availability = Availability(flavor=flavor, user=self.user)
        self.availability.save()

    def test_get_availability(self):
        context = WhichContext()
        context.client_user = self.user
        context.functionality = self.functionality
        get_availability(context)
        self.assertIsNotNone(context.availability)
        self.assertEqual(context.availability, self.availability)


class CheckAvailability(TestCase):
    def test_not_enabled(self):
        context = WhichContext()
        context.availability = Availability(is_enabled=False)
        self.assertIsNone(check_for_existing_enabled_availability(context))

    def test_enabled(self):
        context = WhichContext()
        context.availability = Availability(is_enabled=True)
        self.assertEqual(check_for_existing_enabled_availability(context), context.availability)


class EnableExistingAvailability(TestCase):
    def setUp(self):
        self.user = ClientUser.user_from_object('testuser')
        self.user.save()
        app = App(name='Test App', slug='test-app')
        app.save()
        self.functionality = Functionality(app=app, name='Test Func', slug='test-func',
                                           rollout_strategy=Functionality.DEFINED_BY_RELEASES)
        self.functionality.save()
        flavor = Flavor(name='Flav', slug='flav', functionality=self.functionality)
        flavor.save()
        self.availability = Availability(flavor=flavor, user=self.user)
        self.availability.save()
        self.release = Release(functionality=self.functionality, max_enabled_users=10)
        self.release.save()

    def test_already_enabled(self):
        context = WhichContext()
        context.availability = Availability(is_enabled=True)
        context.functionality = Functionality()
        context.functionality.availability = context.availability
        availability = enable_or_create_availability_by_user_count(context)
        self.assertEqual(availability, context.availability)

    def test_wrong_roll_out_strategy(self):
        context = WhichContext()
        context.availability = Availability(is_enabled=False)
        context.functionality = Functionality(rollout_strategy=Functionality.RECALL_FUNCTIONALITY)
        availability = enable_or_create_availability_by_user_count(context)
        self.assertIsNone(availability)

    def test_enable_with_users_to_spare(self):
        self.release.max_enabled_users = 100
        self.availability.is_enabled = False
        self.release.save()

        context = WhichContext()
        context.availability = self.availability
        context.functionality = self.functionality
        availability = enable_or_create_availability_by_user_count(context)
        self.assertEqual(availability, self.availability)


class AssertExistenceOfFlavors(TestCase):
    def test_with_flavors_present(self):
        app = App(name='Test App', slug='test-app')
        app.save()
        self.functionality = Functionality(app=app, name='Test Func', slug='test-func',
                                           rollout_strategy=Functionality.DEFINED_BY_RELEASES)
        self.functionality.save()
        flavor = Flavor(name='Flav', slug='flav', functionality=self.functionality)
        flavor.save()

        context = WhichContext()
        context.functionality = self.functionality
        self.assertIsNone(assert_existence_of_flavors(context))

    def test_with_no_flavors_present(self):
        context = WhichContext()
        context.functionality = Functionality()

        from core.functionality import NoAvailability
        with self.assertRaises(NoAvailability):
            assert_existence_of_flavors(context)