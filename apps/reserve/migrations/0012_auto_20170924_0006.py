# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 00:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0011_schoolbusreserve_is_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolbus',
            name='num_seats',
            field=models.IntegerField(blank=True, default=47, null=True, verbose_name='总座位数'),
        ),
    ]
