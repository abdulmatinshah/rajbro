# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-10 08:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0006_auto_20161105_0834'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salelineitem',
            old_name='posting_status',
            new_name='posted',
        ),
    ]
