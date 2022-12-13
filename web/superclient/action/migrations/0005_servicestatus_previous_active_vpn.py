# Generated by Django 4.1.1 on 2022-12-13 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vpn', '0021_alter_configuration_name'),
        ('action', '0004_servicestatus_apply'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicestatus',
            name='previous_active_vpn',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous_active_vpn', to='vpn.configuration'),
        ),
    ]
