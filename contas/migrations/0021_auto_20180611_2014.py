# Generated by Django 2.0.4 on 2018-06-11 23:14

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0020_user_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Seu nome será usado para identifica-lo de forma única na plataforma', max_length=50, unique=True, validators=[django.core.validators.RegexValidator(re.compile('/(?=^.{2,60}$)^[A-ZÀÁÂĖÈÉÊÌÍÒÓÔÕÙÚÛÇ][a-zàáâãèéêìíóôõùúç]+(?:[ ](?:das?|dos?|de|e|[A-Z][a-z]+))*$/'), 'Informe um nome de usuário válido', 'este valor deve conter apenas letras e espaços', 'invalid')], verbose_name='nome'),
        ),
    ]
