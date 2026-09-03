# 13. Write a function that accepts a list of numbers and returns their average.

def average(numbers):
    return sum(numbers) / len(numbers)

numbers = list(map(int, input("Enter numbers: ").split()))

print("Average =", average(numbers))