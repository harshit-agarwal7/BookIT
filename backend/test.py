import isbnlib

isbn = '1861972980'
SERVICE = 'goob'
book = isbnlib.meta(isbn)

title = book['Title']
authors = book['Authors']
Publisher = book['Publisher']

print("title:", title)
print(authors)
print(Publisher)
print(book)
