n = int(input("How many numbers: "))

smallest = int(input("Enter number: "))

for i in range(1, n):
    num = int(input("Enter number: "))

    if num < smallest:
        smallest = num

print("Smallest number =", smallest)