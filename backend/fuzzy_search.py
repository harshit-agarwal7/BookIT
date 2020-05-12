from fuzzywuzzy import process


def get_best_five(book_name, book_list):
    results = process.extract(book_name, book_list, limit=5)
    result_book_names = [result[0] for result in results]
    return result_book_names
