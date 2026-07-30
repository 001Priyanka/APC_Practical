n = int(input("How many numbers: "))

largest = int(input("Enter number: "))

for i in range(1, n):
    num = int(input("Enter number: "))

    if num > largest:
        largest = num

print("Largest number =", largest)