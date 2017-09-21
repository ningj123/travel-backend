# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 13:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reserve', '0005_auto_20170921_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolBusTimeSchedules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_schedule', models.CharField(max_length=10, verbose_name='时刻')),
            ],
            options={
                'verbose_name': '发车时间',
                'verbose_name_plural': '发车时间',
            },
        ),
        migrations.CreateModel(
            name='SchoolBusWeekSchedules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField(choices=[(1, '星期一'), (2, '星期二'), (3, '星期三'), (4, '星期四'), (5, '星期五'), (6, '星期六'), (7, '星期天')], verbose_name='星期')),
                ('time', models.ManyToManyField(to='reserve.SchoolBusTimeSchedules', verbose_name='发车时间')),
            ],
            options={
                'verbose_name': '一周发车时刻',
                'verbose_name_plural': '一周发车时刻',
            },
        ),
        migrations.RemoveField(
            model_name='schoolbus',
            name='date_create',
        ),
        migrations.RemoveField(
            model_name='schoolbus',
            name='week',
        ),
        migrations.AddField(
            model_name='schoolbus',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 21, 13, 49, 26, 537822)),
        ),
        migrations.AlterField(
            model_name='schoolbus',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reserve.SchoolBusTimeSchedules', verbose_name='时刻'),
        ),
        migrations.DeleteModel(
            name='SchoolBusSchedules',
        ),
    ]
