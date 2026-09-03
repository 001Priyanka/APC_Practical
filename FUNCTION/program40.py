# 40. Take two lists of numbers, use map() and lambda
#     to create a third list containing the sum of corresponding elements.

list1 = list(map(int, input("Enter first list: ").split()))
list2 = list(map(int, input("Enter second list: ").split()))

result = list(map(lambda x, y: x + y, list1, list2))

print("Result =", result)