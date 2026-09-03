# 25. Create functions to add books, issue books, return books,
#     search books, and display available books.
#     Maintain book availability using dictionaries.

books = {}

def add_book(book_id, title):
    books[book_id] = {
        "title": title,
        "available": True
    }

def issue_book(book_id):
    if book_id in books and books[book_id]["available"]:
        books[book_id]["available"] = False
        print("Book issued.")
    else:
        print("Book not available.")

def return_book(book_id):
    if book_id in books:
        books[book_id]["available"] = True
        print("Book returned.")

def search_book(title):
    for book in books.values():
        if book["title"].lower() == title.lower():
            print("Book found:", book["title"])
            return

    print("Book not found.")

def display_books():
    print("Available Books:")

    for book_id, book in books.items():
        if book["available"]:
            print(book_id, book["title"])

add_book(1, "Python")
add_book(2, "Java")
add_book(3, "C Programming")

issue_book(1)
return_book(1)
search_book("Python")
display_books()