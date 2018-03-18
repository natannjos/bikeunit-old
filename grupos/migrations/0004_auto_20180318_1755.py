# Generated by Django 2.0.3 on 2018-03-18 20:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grupos', '0003_auto_20180318_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupos',
            name='participantes',
            field=models.ManyToManyField(blank=True, related_name='Participantes', to=settings.AUTH_USER_MODEL, verbose_name='Participantes'),
        ),
        migrations.AddField(
            model_name='grupos',
            name='pedais',
            field=models.ManyToManyField(blank=True, to='grupos.Pedal', verbose_name='Pedais'),
        ),
        migrations.AlterField(
            model_name='grupos',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL, verbose_name='Administrador'),
        ),
    ]
