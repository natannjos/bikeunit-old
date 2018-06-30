# Generated by Django 2.0.4 on 2018-06-30 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0030_auto_20180629_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convitedegrupo',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Pendente'), (1, 'Aguardando Aprovação'), (2, 'Aprovado'), (3, 'Regeitado')], default=0, verbose_name='Status'),
        ),
    ]
