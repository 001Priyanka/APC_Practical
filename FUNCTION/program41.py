# 41. Take a list of integers, use filter() and lambda
#     to extract all even numbers.

numbers = list(map(int, input("Enter numbers: ").split()))

even_numbers = list(filter(lambda x: x % 2 == 0, numbers))

print("Even numbers =", even_numbers)