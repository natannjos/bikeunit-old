# Generated by Django 2.0.4 on 2018-06-16 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0007_auto_20180614_0655'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupos',
            name='capa',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Capa'),
        ),
    ]
