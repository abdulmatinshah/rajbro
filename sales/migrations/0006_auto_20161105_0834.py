# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-05 08:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_auto_20161105_0829'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salelineitem',
            old_name='sale_date',
            new_name='sale_order',
        ),
    ]
