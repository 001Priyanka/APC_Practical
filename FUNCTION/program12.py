# 12. Create a function that checks whether a given string or number is a palindrome.

def palindrome(value):
    value = str(value)

    if value == value[::-1]:
        return True
    else:
        return False

value = input("Enter a string or number: ")

print(palindrome(value))