# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-11 23:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_auto_20171111_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='url',
            field=models.URLField(),
        ),
    ]
