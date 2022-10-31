from django.db import models
from superclient.hotspot.models import Profile
from superclient.vpn.models import Configuration



class ServiceStatus(models.Model):

    on = models.BooleanField(default=0)

    active_profile = models.OneToOneField(
        Profile,
        on_delete=models.SET_NULL,
        null=True
    )

    active_vpn = models.OneToOneField(
        Configuration,
        on_delete=models.SET_NULL,
        null=True
    )

    @staticmethod
    def get():
        if ServiceStatus.objects.all().count() == 0:
            status = ServiceStatus.objects.create()
            status.save()

        return ServiceStatus.objects.first()

    def change_active_profile(self, profile):
        self.active_profile = profile
        self.save()

    def change_active_vpn(self, vpn):
        self.active_vpn = vpn
        self.save()

    def toggle_on(self):
        self.on = not self.on
        self.save()
