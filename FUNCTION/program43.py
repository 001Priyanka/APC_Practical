# 43. Use filter() and lambda to extract positive numbers from a list.

numbers = list(map(int, input("Enter numbers: ").split()))

positive = list(filter(lambda x: x > 0, numbers))

print("Positive numbers =", positive)