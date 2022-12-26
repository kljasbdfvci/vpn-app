# Generated by Django 4.1.1 on 2022-12-26 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0023_dhcpserverconfig_bridge'),
    ]

    operations = [
        migrations.AddField(
            model_name='dhcpserverconfig',
            name='mac',
            field=models.CharField(default=None, editable=False, max_length=64),
        ),
        migrations.AddField(
            model_name='hotspotconfig',
            name='mac',
            field=models.CharField(default=None, editable=False, max_length=64),
        ),
        migrations.AddField(
            model_name='lanconfig',
            name='mac',
            field=models.CharField(default=None, editable=False, max_length=64),
        ),
        migrations.AddField(
            model_name='wlanconfig',
            name='mac',
            field=models.CharField(default=None, editable=False, max_length=64),
        ),
    ]
