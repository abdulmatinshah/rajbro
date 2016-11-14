# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-10 09:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0008_auto_20161110_0924'),
        ('products', '0007_auto_20161109_1044'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.AlterField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='customers.Supplier'),
        ),
        migrations.DeleteModel(
            name='Supplier',
        ),
    ]
