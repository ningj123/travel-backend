# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 13:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0002_schoolbus_date_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolbus',
            name='date_create',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='时间'),
        ),
    ]
