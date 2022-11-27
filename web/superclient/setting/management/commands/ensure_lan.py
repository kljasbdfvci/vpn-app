from django.core.management.base import BaseCommand
from ...models import LanConfig

class Command(BaseCommand):
    help = "Creates lan non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        if LanConfig.objects.count() == 0:
            s = LanConfig(id = 1, interface = "eth0", dhcp = True)
            s.save()
