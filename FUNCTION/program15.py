# 15. Write a function that accepts a list and returns a new list containing only unique elements.

def unique_elements(numbers):
    unique = []

    for num in numbers:
        if num not in unique:
            unique.append(num)

    return unique

numbers = list(map(int, input("Enter numbers: ").split()))

print("Unique elements =", unique_elements(numbers))