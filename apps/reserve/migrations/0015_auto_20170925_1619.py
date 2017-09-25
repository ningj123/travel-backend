# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 16:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reserve', '0014_remove_specialcar_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialCarTravel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.IntegerField(choices=[(1, '大花岭'), (2, '街道口'), (3, '光谷'), (4, '武昌站'), (5, '汉口火车站'), (6, '武汉站')], verbose_name='目的地')),
                ('is_done', models.BooleanField(default=False, verbose_name='是否完成')),
            ],
        ),
        migrations.AddField(
            model_name='specialcar',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL, verbose_name='乘坐用户'),
        ),
        migrations.AddField(
            model_name='specialcartravel',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reserve.SpecialCar', verbose_name='专车'),
        ),
        migrations.AddField(
            model_name='specialcartravel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]
