# Generated by Django 4.1.1 on 2022-10-15 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotspot', '0003_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='activeProfile',
        ),
        migrations.AddField(
            model_name='status',
            name='active_profile',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotspot.profile'),
        ),
    ]
