# Generated by Django 2.0.3 on 2018-03-18 21:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0011_user_amigos'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='convites_enviados',
            field=models.ManyToManyField(related_name='_user_convites_enviados_+', to=settings.AUTH_USER_MODEL, verbose_name='Convites Enviados'),
        ),
        migrations.AddField(
            model_name='user',
            name='convites_recebidos',
            field=models.ManyToManyField(related_name='_user_convites_recebidos_+', to=settings.AUTH_USER_MODEL, verbose_name='Convites Recebidos'),
        ),
        migrations.AlterField(
            model_name='user',
            name='amigos',
            field=models.ManyToManyField(related_name='_user_amigos_+', to=settings.AUTH_USER_MODEL, verbose_name='Meus Amigos'),
        ),
    ]