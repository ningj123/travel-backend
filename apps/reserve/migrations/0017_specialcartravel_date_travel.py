# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 17:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0016_auto_20170925_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialcartravel',
            name='date_travel',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='出行时间'),
        ),
    ]
