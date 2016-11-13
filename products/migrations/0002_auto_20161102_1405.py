# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-02 14:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='active',
        ),
        migrations.AddField(
            model_name='product',
            name='discontinued',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity_per_unit',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='sale_rate',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='units_in_stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]