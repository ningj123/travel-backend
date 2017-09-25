# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 13:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20170925_1157'),
        ('reserve', '0012_auto_20170924_0006'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialCar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=20, verbose_name='车牌号')),
                ('num_user', models.IntegerField(default=0, verbose_name='搭乘人数')),
                ('status', models.BooleanField(default=False, help_text='False不能匹配，True可匹配', verbose_name='状态')),
                ('driver', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.Driver', verbose_name='专车司机')),
            ],
            options={
                'verbose_name': '专车',
                'verbose_name_plural': '专车',
            },
        ),
    ]