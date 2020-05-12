"""bookselling URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import bookselling.views as views
import buy_books.views as bb_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="home"),
    url(r'^book_search/', bb_views.book_search, name="book_search"),
    url(r'^my_books/', bb_views.my_books, name="my_books"),
    url(r'^show_book_details/', bb_views.show_book_details, name='show_book_details'),
    url(r'^complaints/', bb_views.complaints, name='complaints'),
    url(r'^sell_form/', bb_views.sell_form, name='sell_form'),
    url(r'^sell_isbn/', bb_views.sell_isbn_search, name='sell_isbn_search'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^order_placed/', bb_views.order_placed, name='order_placed'),
    url(r'^confirm/', bb_views.confirm, name='confirm'),
    url(r'^buyer_transaction_complete/', bb_views.buyer_transaction_complete, name='buyer_transaction_complete'),
    url(r'^seller_transaction_complete/', bb_views.seller_transaction_complete, name='seller_transaction_complete'),
    url(r'^seller_transaction_complete_check/', bb_views.check_transaction_key,
        name='seller_transaction_complete_check'),
    url(r'^payment/$', bb_views.payment, name="payment"),
    url(r'^payment/success$', bb_views.payment_success, name="payment_success"),
    url(r'^payment/failure$', bb_views.payment_failure, name="payment_failure"),
    url(r'^logout/$', bb_views.logout, name='logout'),

    # url(r'^logout/$', auth_views.logout, name='logout'),

]
