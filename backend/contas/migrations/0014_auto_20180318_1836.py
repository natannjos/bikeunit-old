# Generated by Django 2.0.3 on 2018-03-18 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0004_auto_20180318_1755'),
        ('contas', '0013_auto_20180318_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='meus_grupos',
            field=models.ManyToManyField(blank=True, related_name='meus_grupos', to='grupos.Grupos', verbose_name='Meus Grupos'),
        ),
        migrations.AddField(
            model_name='user',
            name='pedais_gratis',
            field=models.ManyToManyField(blank=True, related_name='pedais_gratis', to='grupos.Pedal', verbose_name='Pedais Gratis'),
        ),
    ]