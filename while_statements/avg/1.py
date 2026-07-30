n = int(input("Enter n: "))

sum = 0

for i in range(1, n + 1, 2):
    sum = sum + i

print("Sum of odd numbers =", sum)