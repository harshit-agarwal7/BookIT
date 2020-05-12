from __future__ import unicode_literals
from django.db import models
import datetime
import random


class BookDetails(models.Model):
    book_name = models.CharField(max_length=200, default="")
    book_author = models.CharField(max_length=200, default="")
    book_price = models.IntegerField(default=-1)
    book_edition = models.CharField(max_length=100, default="")
    book_image = models.CharField(max_length=100, default="")
    seller_email = models.CharField(max_length=200, default="")
    date_time_of_listing = models.DateTimeField(default=datetime.datetime.now())
    book_type = models.CharField(max_length=50, default="")
    book_status = models.CharField(max_length=50, default="")
    book_pages = models.IntegerField(default=0)
    book_publisher = models.CharField(max_length=200, default="")
    book_isbn = models.IntegerField(default=0)


class Transactions(models.Model):
    book_id = models.IntegerField(default=-1)
    seller_email = models.CharField(max_length=200, default="")
    buyer_email = models.CharField(max_length=200, default="")
    purchase_date_time = models.DateTimeField(default=datetime.datetime.now())
    book_name = models.CharField(max_length=200, default="")
    book_author = models.CharField(max_length=200, default="")
    book_price = models.IntegerField(default=-1)
    book_edition = models.CharField(max_length=100, default="")
    book_status = models.CharField(max_length=50, default="")
    transaction_key = models.IntegerField(max_length=6, default=-1)


class Complaints(models.Model):
    seller_email = models.CharField(max_length=200)
    buyer_email = models.CharField(max_length=200)
    purchase_date_time = models.DateField(max_length=200)
    book_name = models.CharField(max_length=200)
    book_isbn = models.IntegerField(default=0)
    complaint_nature = models.CharField(max_length=1000)
