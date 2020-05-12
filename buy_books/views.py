import datetime
import random

import isbnlib
from django.core.mail import send_mail
from django.http import Http404

from backend import filter_and_sort, general
from backend import fuzzy_search
from .models import BookDetails, Transactions, Complaints
from django.contrib.auth import logout as auth_logout

def book_search(request):
    query_result = BookDetails.objects.filter(book_status='available')
    book_list = []
    for item in query_result:
        book_list.append(item.book_name)

    if request.method == "POST":
        book_name = request.POST.get("book_query", None)
        filter_request = request.POST.get("filter", None)
        sort_request = request.POST.get("sort", None)
        if book_name is None:
            book_name = ""
        if len(book_name) != 0:
            best_matches = fuzzy_search.get_best_five(book_name, book_list)
            book_details = []
            for book in best_matches:
                for book_object in query_result:
                    if book == book_object.book_name:
                        book_details.append(book_object)
            book_details = general.check_replace_img_path(book_details)
            context = {
                'books': book_details
            }
            return render(request, 'buy_search_browse.html', context)
        else:
            context = {}
            if filter_request is None and sort_request is None:
                query_result = general.check_replace_img_path(query_result)
                context = {
                    'books': query_result
                }
            else:
                book_details = query_result
                if filter_request is not None:
                    book_details = filter_and_sort.filter(query_result, filter_request)
                if sort_request is not None:
                    book_details = filter_and_sort.sort(book_details, sort_request)
                book_details = general.check_replace_img_path(book_details)
                context = {
                    'books': book_details
                }
            return render(request, 'buy_search_browse.html', context)

    else:
        query_result = general.check_replace_img_path(query_result)
        context = {
            'books': query_result
        }
        return render(request, 'buy_search_browse.html', context)


def my_books(request):
    # email = request.user.email
    email = "ayushree.gangal@ashoka.edu.in"
    query_result_transactions = Transactions.objects.all()
    query_result_bookdetails = BookDetails.objects.all()
    books_listed = []
    books_bought = []

    for item in query_result_bookdetails:
        if item.seller_email == email:
            books_listed.append(item)

    for item in query_result_transactions:
        if item.buyer_email == email:
            books_bought.append(item)

    context = {}

    if len(books_listed) > 0:
        context['books_listed'] = books_listed
    if len(books_bought) > 0:
        context['books_bought'] = books_bought

    return render(request, 'my_books.html', context)


def show_book_details(request):
    try:
        id = request.GET.get("buy_value", None)
        book = BookDetails.objects.get(pk=id)
    except BookDetails.DoesNotExist:
        raise Http404("Book does not exist")
    return render(request, 'details.html', {'book': book})


def write_to_transaction(book, buyer_email, id):
    input_seller_email = book.seller_email
    input_buyer_email = buyer_email
    input_purchase_date = datetime.datetime.now()
    input_book_name = book.book_name
    input_book_author = book.book_author
    input_book_price = book.book_price
    input_book_edition = book.book_edition
    input_book_status = book.book_status
    input_transaction_key = random.randint(111111, 1000000)
    input_book_id = id
    transactions_instance = Transactions.objects.create(book_id=input_book_id,
                                                        seller_email=input_seller_email,
                                                        buyer_email=input_buyer_email,
                                                        purchase_date_time=input_purchase_date,
                                                        book_name=input_book_name,
                                                        book_author=input_book_author,
                                                        book_price=input_book_price,
                                                        book_edition=input_book_edition,
                                                        book_status=input_book_status,
                                                        transaction_key=input_transaction_key)
    transactions_instance.save()


def order_placed(request):
    try:
        id = request.POST.get("buy_value", None)
        buyer_email = request.user.email
        book = BookDetails.objects.get(pk=id)
        book.book_status = 'In Progress'
        book.save()
        print(book.book_status)
        write_to_transaction(book, buyer_email, id)
        send_mail(
            'New Order',
            'Hello' + ', \n \n'
                      'Your book, ' + book.book_name + ', has been requested to be bought by ' + buyer_email +
            '. Please contact the person to proceed with the transaction.'  '\n'
            '\n'
            'Best,' '\n'
            'Team: Status-Committed \n',

            'books.ashoka@gmail.com',
            [book.seller_email],
            fail_silently=False,
        )
        send_mail(
            'Order Placed',
            'Hello ' + ', \n \n'
                       'You have ordered the book, ' + book.book_name + '. You will be contacted by the seller( ' +
            book.seller_email + ' ) soon.'  '\n'
                                '\n'
                                'Best,' '\n'
                                'Team: Status-Committed \n',

            'books.ashoka@gmail.com',
            [buyer_email],
            fail_silently=False,
        )
    except BookDetails.DoesNotExist:
        raise Http404("Book does not exist")
    return redirect('/my_books/')


def confirm(request):
    try:
        id = request.GET.get("buy_value", None)
        book = BookDetails.objects.get(pk=id)
    except BookDetails.DoesNotExist:
        raise Http404("Book does not exist")
    return render(request, 'confirm.html', {'book': book})


def complaints(request):
    if request.method == "POST":
        input_buyer_email = "ayushree.gangal@ashoka.edu.in"
        input_seller_email = request.POST.get("seller_email", None)
        input_book_name = request.POST.get("book_name", None)
        input_book_isbn = request.POST.get("book_isbn", None)
        input_nature_of_complaint = request.POST.get("complaint", None)
        input_purchase_date = request.POST.get("purchase_date", None)
        complaints_instance = Complaints.objects.create(buyer_email=input_buyer_email,
                                                        seller_email=input_seller_email,
                                                        purchase_date_time=input_purchase_date,
                                                        book_name=input_book_name,
                                                        book_isbn=input_book_isbn,
                                                        complaint_nature=input_nature_of_complaint)
        complaints_instance.save()
        return render(request, 'index.html')
    else:
        return render(request, 'complaints.html')


def sell_form(request):
    if request.method == "POST":
        input_book_name = request.POST.get("book_name", None)
        if input_book_name is None:
            input_book_name = request.POST.get("book_name_hidden", None)
        input_book_author = request.POST.get("book_author", None)
        if input_book_author is None:
            input_book_author = request.POST.get("book_author_hidden", None)
        input_book_price = request.POST.get("book_price", None)
        input_book_edition = request.POST.get("book_edition", None)
        input_seller_email = "ayushree.gangal@ashoka.edu.in"
        input_book_type = request.POST.get("book_type", None)
        input_book_status = "available"
        input_book_isbn = request.POST.get("book_isbn", None)
        if input_book_isbn is None:
            input_book_isbn = request.POST.get("book_isbn_hidden", None)
        input_book_pages = request.POST.get("book_pages", None)
        input_book_publisher = request.POST.get("book_publisher", None)
        if input_book_publisher is None:
            input_book_publisher = request.POST.get("book_publisher_hidden", None)
        input_date_time_of_listing = datetime.datetime.now()
        book_details_instance = BookDetails.objects.create(book_name=input_book_name,
                                                           book_author=input_book_author,
                                                           book_price=input_book_price,
                                                           book_edition=input_book_edition,
                                                           seller_email=input_seller_email,
                                                           book_type=input_book_type,
                                                           book_status=input_book_status,
                                                           book_isbn=input_book_isbn,
                                                           book_pages=input_book_pages,
                                                           book_publisher=input_book_publisher,
                                                           date_time_of_listing=input_date_time_of_listing
                                                           )
        book_details_instance.save()
        return render(request, 'index.html')
    else:
        return render(request, 'sell_input.html')


def sell_isbn_search(request):
    if request.method == "POST":
        input_isbn = request.POST.get("book_isbn", None)
        if len(input_isbn) < 10 or len(input_isbn) == 11 or len(input_isbn) == 12 or len(input_isbn) > 13:
            input_isbn = ""
        if input_isbn is None:
            input_isbn = ""
        if len(input_isbn) != 0:
            try:
                book = isbnlib.meta(input_isbn)
                book_details = []
                context = {}
                if book is not None:
                    if book['Title'] is not None:
                        context = book
                        context['isbn'] = input_isbn
                        return render(request, 'sell_input.html', context)
                    else:
                        return render(request, 'sell_input.html')
                else:
                    return render(request, 'sell_input.html')
            except:
                return render(request, 'sell_input.html')
        else:
            return render(request, 'sell_input.html')
    else:
        return render(request, 'sell.html')


def buyer_transaction_complete(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id", None)
        book = BookDetails.objects.get(pk=book_id)
        book_transaction = Transactions.objects.get(book_id=book_id)
        key = book_transaction.transaction_key
        context = {
            'book': book,
            'key': key
        }
        return render(request, 'buyer_complete_transaction.html', context)
    else:
        return redirect('/my_books/')


def seller_transaction_complete(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id", None)
        book = BookDetails.objects.get(pk=book_id)
        context = {}
        context['book'] = book
        return render(request, 'seller_complete_transaction.html', context)
    else:
        return redirect('/my_books/')


def check_transaction_key(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id", None)
        input_key = int(request.POST.get("book_transaction_key", None))
        book = Transactions.objects.get(book_id=book_id)
        key_in_table = book.transaction_key
        if key_in_table == input_key:
            book.book_status = "Sold"
            book.save()
            book_bookdetails = BookDetails.objects.get(pk=book_id)
            book_bookdetails.book_status = "Sold"
            book_bookdetails.save()
            return redirect('/my_books/')
        else:
            book = BookDetails.objects.get(pk=book_id)
            context = {}
            context['book'] = book
            context['error'] = "Incorrect OTP. Please try again!"
            return render(request, 'seller_complete_transaction.html', context)


from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import logging, traceback
import buy_books.constants as constants
import buy_books.config as config
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_exempt


def payment(request):
    data = {}
    txnid = get_transaction_id()
    hash_ = generate_hash(request, txnid)
    hash_string = get_hash_string(request, txnid)
    # use constants file to store constant values.
    # use test URL for testing
    data["action"] = constants.PAYMENT_URL_LIVE
    data["amount"] = float(constants.PAID_FEE_AMOUNT)
    data["productinfo"] = constants.PAID_FEE_PRODUCT_INFO
    data["key"] = config.KEY
    data["txnid"] = txnid
    data["hash"] = hash_
    data["hash_string"] = hash_string
    data["firstname"] = ""
    data["email"] = ""
    data["phone"] = ""
    data["service_provider"] = constants.SERVICE_PROVIDER
    data["furl"] = request.build_absolute_uri(reverse("payment_failure"))
    data["surl"] = request.build_absolute_uri(reverse("payment_success"))

    return render(request, "payment.html", data)


# generate the hash
def generate_hash(request, txnid):
    try:
        # get keys and SALT from dashboard once account is created.
        # hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        hash_string = get_hash_string(request, txnid)
        generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        return generated_hash
    except Exception as e:
        # log the error here.
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


# create hash string using all the fields
def get_hash_string(request, txnid):
    hash_string = config.KEY + "|" + txnid + "|" + str(
        float(constants.PAID_FEE_AMOUNT)) + "|" + constants.PAID_FEE_PRODUCT_INFO + "|"
    hash_string += "" + "|" + "" + "|"
    hash_string += "||||||||||" + config.SALT

    return hash_string


# generate a random transaction Id.
def get_transaction_id():
    hash_object = hashlib.sha256(str(randint(0, 9999)).encode("utf-8"))
    # take approprite length
    txnid = hash_object.hexdigest().lower()[0:32]
    return txnid


# no csrf token require to go to Success page.
# This page displays the success/confirmation message to user indicating the completion of transaction.
@csrf_exempt
def payment_success(request):
    data = {}
    return render(request, "sucess.html", data)


# no csrf token require to go to Failure page. This page displays the message and reason of failure.
@csrf_exempt
def payment_failure(request):
    data = {}
    return render(request, "failure.html", data)


def logout(request):
    auth_logout(request)
    for sesskey in request.session.keys():
        del request.session[sesskey]
    return render(request, 'index.html')
