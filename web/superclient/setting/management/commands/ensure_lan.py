from django.core.management.base import BaseCommand
from ...models import LanConfig
from ...service.network import *

class Command(BaseCommand):
    help = "Creates lan non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        if LanConfig.objects.count() == 0:
            s = LanConfig(interface = get_first_eth_interface())
            s.save()
