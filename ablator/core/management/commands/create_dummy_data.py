import random
import string

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from core.models import App, Functionality, Flavor, Release, ClientUser
from core.functionality import which

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
        for app_name in app_names:
            app = App(name=app_name, slug=slugify(app_name))
            app.save()
            self.stdout.write(self.style.SUCCESS('### Created App {} ###'.format(app.name)))

            for f_name in functionality_descriptions.keys():
                functionality = Functionality(app=app, name=f_name, slug=slugify(f_name))
                functionality.save()
                self.stdout.write(self.style.SUCCESS('Created Functionality {}'.format(functionality.name)))
                release = Release(functionality=functionality, max_enabled_users=6)
                release.save()
                self.stdout.write(self.style.SUCCESS(' + Release {}'.format(release.name)))
                for flavor_name in functionality_descriptions[f_name]:
                    flavor = Flavor(name=flavor_name, slug=slugify(flavor_name))
                    flavor.functionality = functionality
                    flavor.save()
                    self.stdout.write(self.style.SUCCESS(' + Flavor {}'.format(flavor.name)))
                num_availabilities = random.randrange(13, 15)
                self.stdout.write('   Generating {} availabilities...'.format(num_availabilities))
                for _ in range(num_availabilities):
                    which(
                        client_user=ClientUser.user_from_object(random_user_name()),
                        functionality=functionality
                    )
                self.stdout.write(self.style.SUCCESS(' + {} availabilities'.format(num_availabilities)))
        self.stdout.write(self.style.SUCCESS('Done :)'))

