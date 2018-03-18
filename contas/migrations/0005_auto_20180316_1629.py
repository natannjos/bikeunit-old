# Generated by Django 2.0.3 on 2018-03-16 19:29

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0004_remove_user_complemento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cep',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(re.compile('^[(\\.](\\d{2})[)\\.]?(\\d{4,5})[-\\.]?(\\d{4})$'))], verbose_name='CEP'),
        ),
    ]