# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='can_apply',
            field=models.BooleanField(default=True, verbose_name='能否预约'),
        ),
        migrations.AddField(
            model_name='user',
            name='usertype',
            field=models.IntegerField(choices=[(1, '司机'), (2, '非司机')], default=2, verbose_name='用户类型'),
        ),
    ]
