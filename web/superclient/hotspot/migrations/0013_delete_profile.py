# Generated by Django 4.1.1 on 2022-11-28 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotspot', '0012_remove_profile_dns'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
