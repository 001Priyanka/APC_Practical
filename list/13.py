numbers = []

print("Enter 10 numbers:")

for i in range(10):
    num = int(input())
    numbers.append(num)

ascending = numbers.copy()
ascending.sort()

descending = numbers.copy()
descending.sort(reverse=True)

print("Ascending Order:", ascending)
print("Descending Order:", descending)