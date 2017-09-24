# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 22:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20170922_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='ucenterreservewrapper',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
