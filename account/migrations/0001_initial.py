# Generated by Django 2.2 on 2019-06-06 08:44

import account.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('total_bandwidth', models.BigIntegerField(verbose_name='total_bandwidth')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_consumed', models.BigIntegerField(verbose_name='amount_consumed')),
                ('active_plan', models.ForeignKey(on_delete=models.SET(account.models.get_sentinel_plan), to='account.Plan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]