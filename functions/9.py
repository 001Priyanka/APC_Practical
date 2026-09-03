def largest(numbers):
    largest = numbers[0]

    for num in numbers:
        if num > largest:
            largest = num

    return largest

print(largest([10, 25, 7, 40, 15]))