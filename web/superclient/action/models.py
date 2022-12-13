from django.db import models
from superclient.vpn.models import Configuration



class ServiceStatus(models.Model):

    on = models.BooleanField(default=False)

    apply = models.BooleanField(default=False)

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

    previous_active_vpn = models.OneToOneField(
        Configuration,
        on_delete=models.SET_NULL,
        null=True,
        related_name='previous_active_vpn',
    )

    @staticmethod
    def get():
        if ServiceStatus.objects.all().count() == 0:
            status = ServiceStatus.objects.create()
            status.save()

        return ServiceStatus.objects.first()

    def change_active_vpn(self, vpn):
        self.previous_active_vpn = self.active_vpn
        self.active_vpn = vpn
        self.save()

    def change_selected_vpn(self, vpn):
        self.selected_vpn = vpn
        self.save()

    def toggle_on(self):
        self.on = not self.on
        self.save()

    def toggle_apply(self):
        self.apply = not self.apply
        self.save()
