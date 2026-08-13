numbers = []

for i in range(5):
    n = int(input("Enter number: "))
    numbers.append(n)

numbers = tuple(numbers)

print("Tuple:", numbers)