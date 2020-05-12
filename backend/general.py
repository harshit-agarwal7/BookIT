def check_replace_img_path(query_result):
    book_details = []
    for book in query_result:
        if book.book_image == "" or book.book_image is None:
            book.book_image = "/static/images/books/no_book_cover.jpg"
        book_details.append(book)
    return book_details
