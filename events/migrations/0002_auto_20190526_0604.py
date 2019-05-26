# Generated by Django 2.2 on 2019-05-26 06:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='due',
            field=models.DateTimeField(default=datetime.date.today, verbose_name='due'),
        ),
        migrations.AlterField(
            model_name='event',
            name='text',
            field=models.TextField(verbose_name='text'),
        ),
    ]