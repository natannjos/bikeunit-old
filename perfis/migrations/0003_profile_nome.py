# Generated by Django 2.0.4 on 2018-06-07 16:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0002_auto_20180508_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='nome',
            field=models.CharField(default=django.utils.timezone.now, max_length=255, verbose_name='Nome Completo'),
            preserve_default=False,
        ),
    ]