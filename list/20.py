books = ["Python", "Java", "C++"]

# Add new book
new_book = input("Enter new book: ")
books.append(new_book)

# Search book
search = input("Enter book to search: ")

if search in books:
    print("Book Found")
else:
    print("Book Not Found")

# Remove book
remove = input("Enter book to remove: ")

if remove in books:
    books.remove(remove)

print("Book List:", books)
print("Total Books:", len(books))