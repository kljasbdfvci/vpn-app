from django.core.management.base import BaseCommand
from ...models import HotspotConfig
from ...service.network import *

class Command(BaseCommand):
    help = "Creates lan non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        if HotspotConfig.objects.count() == 0:
            s = HotspotConfig(id = 1, interface = get_first_wlan_interface(), ssid = "Power Freenet", wpa_passphrase = "12345678")
            s.save()
