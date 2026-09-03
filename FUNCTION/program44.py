# 44. Take a list of numbers, use filter() and lambda
#     to find numbers greater than 50.

numbers = list(map(int, input("Enter numbers: ").split()))

result = list(filter(lambda x: x > 50, numbers))

print("Numbers greater than 50 =", result)