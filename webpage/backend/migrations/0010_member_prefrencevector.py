# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 19:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_auto_20161201_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='prefrenceVector',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
