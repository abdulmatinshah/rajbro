# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-16 04:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0013_auto_20161114_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Customer'),
        ),
    ]
