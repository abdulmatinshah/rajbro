# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-20 07:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0018_sale_post_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='post_items',
        ),
    ]
