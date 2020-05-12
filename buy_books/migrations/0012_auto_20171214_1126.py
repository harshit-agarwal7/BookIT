# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-14 11:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buy_books', '0011_auto_20171214_0700'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='book_status',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='bookdetails',
            name='date_time_of_listing',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 14, 11, 26, 23, 268740)),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='purchase_date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 14, 11, 26, 23, 270439)),
        ),
    ]
