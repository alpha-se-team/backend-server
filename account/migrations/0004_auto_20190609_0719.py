# Generated by Django 2.2 on 2019-06-09 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20190609_0625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='amount_consumed',
            field=models.BigIntegerField(default=0, verbose_name='amount_consumed'),
        ),
    ]
