# Generated by Django 2.2 on 2019-05-24 11:33

from django.db import migrations, models
import events.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_as')),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('text', models.TextField(verbose_name='content')),
                ('img', models.ImageField(upload_to='', validators=[events.models.image_size_valid], verbose_name='img')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
