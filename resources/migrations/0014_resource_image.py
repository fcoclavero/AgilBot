# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 19:46
from __future__ import unicode_literals

from django.db import migrations, models
import resources.models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0013_auto_20171115_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=resources.models.image_filename),
        ),
    ]
