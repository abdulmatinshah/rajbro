# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-09 11:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0012_auto_20161109_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Rs.', max_digits=100),
        ),
    ]