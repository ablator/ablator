from django.test import TestCase

from core.functionality import WhichContext
from core.functionality.availability import check_for_existing_enabled_availability, \
    get_availability, \
    enable_availability_by_user_count, _availability_or_none, \
    assert_existence_of_flavors
from core.models import Availability, ClientUser, Functionality, App, Flavor, Release
from user_management.models import Company


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
        self.company = Company(name='Testcompany')
        self.company.save()
        self.user = ClientUser.user_from_object('testuser')
        self.user.save()
        app = App(name='Test App', slug='test-app', company=self.company)
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
        self.company = Company(name='Testcompany')
        self.company.save()
        self.user = ClientUser.user_from_object('testuser')
        self.user.save()
        app = App(name='Test App', slug='test-app', company=self.company)
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
        availability = enable_availability_by_user_count(context)
        self.assertEqual(availability, context.availability)

    def test_wrong_roll_out_strategy(self):
        context = WhichContext()
        context.availability = Availability(is_enabled=False)
        context.functionality = Functionality(rollout_strategy=Functionality.RECALL_FUNCTIONALITY)
        availability = enable_availability_by_user_count(context)
        self.assertIsNone(availability)

    def test_enable_with_users_to_spare(self):
        context = WhichContext()
        context.availability = self.availability
        context.functionality = self.functionality
        context.enabled_count = 5
        availability = enable_availability_by_user_count(context)
        self.assertEqual(availability, self.availability)


class AssertExistenceOfFlavors(TestCase):
    def test_with_flavors_present(self):
        company = Company(name='Testcompany')
        company.save()
        app = App(name='Test App', slug='test-app', company=company)
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