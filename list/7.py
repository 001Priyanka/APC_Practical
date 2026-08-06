numbers = []

for i in range(10):
    num = int(input("Enter number: "))
    numbers.append(num)

total = sum(numbers)
average = total / len(numbers)

print("List:", numbers)
print("Sum:", total)
print("Average:", average)