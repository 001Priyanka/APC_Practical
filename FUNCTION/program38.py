# 38. Take a list of numbers, use map() and a lambda function
#     to generate a list containing their squares.

numbers = list(map(int, input("Enter numbers: ").split()))

squares = list(map(lambda x: x * x, numbers))

print("Squares =", squares)