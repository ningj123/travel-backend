# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0022_auto_20170928_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialcartimeschedule',
            name='endtime',
            field=models.TimeField(blank=True, verbose_name='结束时间'),
        ),
        migrations.AlterField(
            model_name='specialcartimeschedule',
            name='starttime',
            field=models.TimeField(verbose_name='起始时间'),
        ),
    ]
