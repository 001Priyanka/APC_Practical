def count_occurrences(numbers, element):
    count = 0

    for num in numbers:
        if num == element:
            count += 1

    return count

print(count_occurrences([1, 2, 2, 3, 2, 4], 2))