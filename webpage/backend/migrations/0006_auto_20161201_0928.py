# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_anime_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tid', models.IntegerField()),
                ('tagName', models.CharField(default=b'', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='anime',
            name='tags',
            field=models.ManyToManyField(to='backend.Tag'),
        ),
    ]