from django.core.management.base import BaseCommand
from ...models import DhcpServerConfig
from ...service.network import *

class Command(BaseCommand):
    help = "Creates lan non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        if DhcpServerConfig.objects.count() == 0:
            s = DhcpServerConfig(interface = get_first_wlan_interface())
            s.save()
