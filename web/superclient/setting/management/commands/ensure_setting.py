from django.core.management.base import BaseCommand
from ...models import Setting

class Command(BaseCommand):
    help = "Creates setting non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        if Setting.objects.count() == 0:
            s = Setting(id=1)
            s.save()
