# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-01 14:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0021_merge_20171123_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='chat_id',
            field=models.BigIntegerField(verbose_name='chat ID'),
        ),
    ]
