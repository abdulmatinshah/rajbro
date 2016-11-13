# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-10 09:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(blank=True, max_length=13, null=True)),
                ('address', models.CharField(blank=True, max_length=180, null=True)),
                ('route_tag', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(blank=True, max_length=13, null=True)),
                ('address', models.CharField(blank=True, max_length=180, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]