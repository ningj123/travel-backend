# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0003_auto_20170921_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolbusschedules',
            name='date_schedule',
            field=models.DateField(),
        ),
    ]
