# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 13:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0013_specialcar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specialcar',
            name='number',
        ),
    ]
