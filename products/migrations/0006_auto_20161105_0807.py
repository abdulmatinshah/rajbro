# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-05 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20161104_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity_per_unit',
            field=models.PositiveIntegerField(default=1, help_text='No.'),
        ),
    ]
