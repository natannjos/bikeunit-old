# Generated by Django 2.0.3 on 2018-03-16 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0003_auto_20180316_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='complemento',
        ),
    ]
