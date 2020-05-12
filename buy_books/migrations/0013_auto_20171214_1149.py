# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-14 11:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buy_books', '0012_auto_20171214_1126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookdetails',
            name='book_id',
        ),
        migrations.AddField(
            model_name='transactions',
            name='book_id',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='bookdetails',
            name='date_time_of_listing',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 14, 11, 49, 55, 114612)),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='purchase_date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 14, 11, 49, 55, 115425)),
        ),
    ]
