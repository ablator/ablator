import random
import string

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import App, Functionality, Flavor, Release, ClientUser
from core.functionality import which
from user_management.models import Organization, AblatorUser

app_names = [
    'Rover',
    'Ascent Vehicle',
    'Long Distance Ship',
]

functionality_descriptions = {
    'Atmospheric Regulator': ['enabled', 'disabled', 'power save mode'],
    'Dehumidifier': ['dry as bone', 'pleasant', 'humid'],
    'Water Reclaimer': ['overdrive', 'drinking water only', 'fizzy'],
    'Space Heater': ['loud', 'power save mode', 'off'],
}


def random_user_name():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


class Command(BaseCommand):
    help = 'Creates dummy Applications, Functionalities and so on'

    def handle(self, *args, **options):
        organization = Organization(name='Masa', slug='masa')
        organization.save()
        self.stdout.write(self.style.SUCCESS('### Created Organization {} ###'.format(organization.name)))

        try:
            first_user = User.objects.all()[0]
            ablator_user = AblatorUser(user=first_user, organization=organization)
            ablator_user.save()
            self.stdout.write(self.style.SUCCESS('### Created User {} ###'.format(ablator_user)))
        except IndexError:
            self.stdout.write('No users yet, skipping user creation')

        for app_name in app_names:
            app = App(name=app_name, slug=slugify(app_name), organization=organization)
            app.save()
            self.stdout.write(self.style.SUCCESS('### Created App {} ###'.format(app.name)))

            for f_name in functionality_descriptions.keys():
                functionality = Functionality(app=app, name=f_name, slug=slugify(f_name))
                functionality.save()
                self.stdout.write(self.style.SUCCESS('Created Functionality {}'.format(functionality.name)))
                release = Release(functionality=functionality, max_enabled_users=6)
                release.save()
                self.stdout.write(self.style.SUCCESS(' + Release {}'.format(release.id)))
                for flavor_name in functionality_descriptions[f_name]:
                    flavor = Flavor(name=flavor_name, slug=slugify(flavor_name))
                    flavor.functionality = functionality
                    flavor.save()
                    self.stdout.write(self.style.SUCCESS(' + Flavor {}'.format(flavor.name)))
                num_availabilities = random.randrange(13, 15)
                for _ in range(num_availabilities):
                    which(
                        client_user=ClientUser.user_from_object(random_user_name()),
                        functionality=functionality
                    )
                self.stdout.write(self.style.SUCCESS(' + {} availabilities'.format(num_availabilities)))
        self.stdout.write(self.style.SUCCESS('Done :)'))
