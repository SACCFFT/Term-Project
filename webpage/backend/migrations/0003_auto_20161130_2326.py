# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-30 23:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20161130_2326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aid', models.IntegerField()),
                ('title', models.CharField(default=b'', max_length=200)),
                ('type', models.CharField(default=b'', max_length=200)),
                ('episodes', models.IntegerField()),
                ('status', models.CharField(default=b'', max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]