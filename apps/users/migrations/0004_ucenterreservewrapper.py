# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 21:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_driver'),
    ]

    operations = [
        migrations.CreateModel(
            name='UcenterReserveWrapper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reserve_pk', models.IntegerField()),
                ('reserve_type', models.IntegerField(choices=[(1, '校车'), (2, '专车')])),
                ('reserve_status', models.IntegerField(choices=[(1, '进行中'), (2, '已完成')])),
            ],
        ),
    ]
