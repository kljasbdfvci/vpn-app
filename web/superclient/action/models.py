from django.db import models
from superclient.hotspot.models import Profile
from superclient.vpn.models import Configuration



class ServiceStatus(models.Model):

    on = models.BooleanField(default=False)

    selected_profile = models.OneToOneField(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='selected_prof',
    )

    active_profile = models.OneToOneField(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='active_prof',
    )

    selected_vpn = models.OneToOneField(
        Configuration,
        on_delete=models.SET_NULL,
        null=True,
        related_name='selected_vpn',
    )

    active_vpn = models.OneToOneField(
        Configuration,
        on_delete=models.SET_NULL,
        null=True,
        related_name='active_vpn',
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

    def change_selected_profile(self, profile):
        self.selected_profile = profile
        self.save()

    def change_selected_vpn(self, vpn):
        self.selected_vpn = vpn
        self.save()

    def toggle_on(self):
        self.on = not self.on
        self.save()
