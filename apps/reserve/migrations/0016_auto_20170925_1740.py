# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 17:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0015_auto_20170925_1619'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='specialcartravel',
            options={'verbose_name': '专车出行申请', 'verbose_name_plural': '专车出行申请'},
        ),
        migrations.AlterField(
            model_name='specialcar',
            name='users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='乘坐用户'),
        ),
    ]