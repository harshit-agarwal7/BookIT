def filter(query_result, filter_request):
    if filter_request == "all":
        return query_result
    else:
        book_details = [book for book in query_result if book.book_type == filter_request]
        return book_details

def sort(query_result, sort_request):
    if "price" in sort_request:
        query_result = sorted(query_result, key=lambda x: x.book_price)
    if "listing" in sort_request:
        query_result = sorted(query_result, key=lambda x: x.date_time_of_listing)
    if "descending" in sort_request:
        query_result.reverse()
    return query_result
