# 22. Write a function that accepts a list of numbers and returns
#     the minimum, maximum, sum, and average.

def statistics(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    total = sum(numbers)
    avg = total / len(numbers)

    return minimum, maximum, total, avg

numbers = list(map(int, input("Enter numbers: ").split()))

minimum, maximum, total, avg = statistics(numbers)

print("Minimum =", minimum)
print("Maximum =", maximum)
print("Sum =", total)
print("Average =", avg)