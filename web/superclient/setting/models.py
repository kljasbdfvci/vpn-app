from django.db import models

# Create your models here.
class Setting(models.Model):
    
    class DnsMode(models.TextChoices):
        _1 = "_1", "Do Nothing"
        _2 = "_2", "Handle in system"
        _3 = "_3", "Handle in hotspot"
        _4 = "_4", "Handle with socks (only for v2ray)"
        
    dns_Mode = models.CharField(max_length=8, choices=DnsMode.choices, default=DnsMode._2)
    dns = models.CharField(max_length=128, default='1.1.1.1,8.8.8.8,208.67.222.222', blank=True)

    def save(self, *args, **kwargs):
        self.dns = "".join(self.dns.split())
        super(Setting, self).save(*args, **kwargs)
