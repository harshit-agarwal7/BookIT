from __future__ import unicode_literals
from django.db import models


class BookDetails(models.Model):
    book_name = models.CharField(max_length=200)
    book_author = models.CharField(max_length=200)
    book_price = models.IntegerField(default=0)
    book_edition = models.CharField(max_length=100)
    seller_email = models.CharField(max_length=200)
    date_time_of_listing = models.DateTimeField()
    book_image = models.CharField(max_length=500)
    book_status = models.CharField(max_length=200)
    book_type = models.CharField(max_length=50)
    book_pages = models.IntegerField(default=0)
    book_publisher = models.CharField(max_length=200)
    book_isbn = models.IntegerField(default=0)
    book_id = models.IntegerField(default=0)


class Transactions(models.Model):
    seller_email = models.CharField(max_length=200)
    buyer_email = models.CharField(max_length=200)
    purchase_date_time = models.DateTimeField()
    book_name = models.CharField(max_length=200)
    book_author = models.CharField(max_length=200)
    book_price = models.IntegerField(default=0)
    book_edition = models.CharField(max_length=100)


class Complaints(models.Model):
    seller_email = models.CharField(max_length=200)
    buyer_email = models.CharField(max_length=200)
    purchase_date_time = models.CharField(max_length=200)
    book_name = models.CharField(max_length=200)
    book_isbn = models.IntegerField(default=0)
    complaint_nature = models.CharField(max_length=1000)


class Foo(models.Model):
    name = models.CharField(max_length=100)
