# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-30 23:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20161130_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
