numbers = []

print("Enter 15 integers:")

for i in range(15):
    num = int(input())
    numbers.append(num)

even = 0
odd = 0

for num in numbers:
    if num % 2 == 0:
        even += 1
    else:
        odd += 1

print("Even numbers:", even)
print("Odd numbers:", odd)