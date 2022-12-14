# Generated by Django 4.1.1 on 2022-12-14 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0017_alter_dhcpserverconfig_dhcp_module'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wlanconfig',
            old_name='ssid',
            new_name='ssid1',
        ),
        migrations.RemoveField(
            model_name='wlanconfig',
            name='wpa_passphrase',
        ),
        migrations.AddField(
            model_name='wlanconfig',
            name='country_code',
            field=models.CharField(default='CN', max_length=8),
        ),
        migrations.AddField(
            model_name='wlanconfig',
            name='ssid2',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='wlanconfig',
            name='ssid3',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='wlanconfig',
            name='ssid4',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='wlanconfig',
            name='wpa_passphrase1',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='wlanconfig',
            name='wpa_passphrase2',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='wlanconfig',
            name='wpa_passphrase3',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='wlanconfig',
            name='wpa_passphrase4',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='hotspotconfig',
            name='country_code',
            field=models.CharField(default='CN', max_length=8),
        ),
    ]
