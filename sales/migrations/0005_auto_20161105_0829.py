# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-05 08:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_auto_20161105_0828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salelineitem',
            name='linetotal',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Rs.', max_digits=100),
        ),
    ]
