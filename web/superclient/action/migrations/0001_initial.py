# Generated by Django 4.1.1 on 2022-10-30 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hotspot', '0005_alter_profile_dhcp_ip_from_alter_profile_dhcp_ip_to_and_more'),
        ('vpn', '0004_configuration_enable'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('on', models.BooleanField(default=0)),
                ('active_profile', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotspot.profile')),
                ('active_vpn', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vpn.configuration')),
            ],
        ),
    ]
