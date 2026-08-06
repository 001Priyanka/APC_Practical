numbers = [10, 20, 30, 20, 40, 10, 50, 30]

unique = []

for num in numbers:
    if num not in unique:
        unique.append(num)

print("Original List:", numbers)
print("Unique Elements:", unique)