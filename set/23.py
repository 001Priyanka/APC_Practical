available_books = {
    "Python Programming",
    "Java Programming",
    "Data Structures",
    "Operating Systems"
}

requested_books = {
    "Python Programming",
    "Data Structures",
    "Machine Learning"
}

available_requested = available_books.intersection(requested_books)

print("Requested books that are available:", available_requested)