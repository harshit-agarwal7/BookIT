# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-07 06:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buy_books', '0007_auto_20171207_0530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookdetails',
            name='date_time_of_listing',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 7, 6, 43, 49, 657381)),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='purchase_date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 7, 6, 43, 49, 658655)),
        ),
    ]
