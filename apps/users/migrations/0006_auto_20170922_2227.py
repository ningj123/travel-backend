# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 22:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20170922_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ucenterreservewrapper',
            name='reserve_status',
            field=models.BooleanField(default=False),
        ),
    ]
