# -*- coding: utf-8 -*-
# Generated by Django 1.11rc1 on 2017-10-16 22:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0002_auto_20171016_2342'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='text',
            field=models.TextField(default=''),
        ),
    ]
