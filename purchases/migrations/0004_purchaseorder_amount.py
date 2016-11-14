# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-04 13:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0003_auto_20161104_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=33, help_text='Rs.', max_digits=100),
            preserve_default=False,
        ),
    ]
