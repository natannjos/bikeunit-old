# Generated by Django 2.0.3 on 2018-03-18 21:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0010_auto_20180316_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='amigos',
            field=models.ManyToManyField(related_name='_user_amigos_+', to=settings.AUTH_USER_MODEL, verbose_name='Amigos'),
        ),
    ]