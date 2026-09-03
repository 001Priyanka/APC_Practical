def is_palindrome(value):
    value = str(value)

    return value == value[::-1]

print(is_palindrome("madam"))
print(is_palindrome(121))