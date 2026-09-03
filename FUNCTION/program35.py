# 35. Write a lambda function that returns True if a number is even
#     and False otherwise.

even = lambda x: x % 2 == 0

n = int(input("Enter number: "))

print(even(n))