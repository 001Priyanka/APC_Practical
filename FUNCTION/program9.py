# 9. Write a function that accepts a list of numbers and returns the largest element
#    without using the built-in max() function.

def largest(numbers):
    large = numbers[0]

    for num in numbers:
        if num > large:
            large = num

    return large

numbers = list(map(int, input("Enter numbers: ").split()))

print("Largest =", largest(numbers))