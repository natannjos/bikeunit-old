# Generated by Django 2.0.4 on 2018-06-14 09:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0006_auto_20180614_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupos',
            name='participantes',
            field=models.ManyToManyField(blank=True, related_name='participantes', to=settings.AUTH_USER_MODEL, verbose_name='Participantes'),
        ),
    ]
