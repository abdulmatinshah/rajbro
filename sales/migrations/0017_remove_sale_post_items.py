# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 15:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0016_auto_20161117_1242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='post_items',
        ),
    ]