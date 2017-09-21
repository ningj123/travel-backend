# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 13:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolBus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField(choices=[(1, '星期一'), (2, '星期二'), (3, '星期三'), (4, '星期四'), (5, '星期五'), (6, '星期六'), (7, '星期天')], verbose_name='星期')),
                ('num_reserve', models.IntegerField(default=0, verbose_name='预约人数')),
                ('num_seats', models.IntegerField(blank=True, verbose_name='总座位数')),
            ],
            options={
                'verbose_name': '校车班次',
                'verbose_name_plural': '校车班次',
            },
        ),
        migrations.CreateModel(
            name='SchoolBusSchedules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_schedule', models.DateTimeField()),
            ],
            options={
                'verbose_name': '发车时刻',
                'verbose_name_plural': '发车时刻',
            },
        ),
        migrations.AddField(
            model_name='schoolbus',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reserve.SchoolBusSchedules', verbose_name='时刻'),
        ),
    ]
