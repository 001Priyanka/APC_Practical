def average(numbers):
    total = 0

    for num in numbers:
        total += num

    return total / len(numbers)

print(average([10, 20, 30, 40, 50]))