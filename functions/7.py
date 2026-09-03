def natural_sum(n):
    total = 0

    for i in range(1, n + 1):
        total += i

    return total

print(natural_sum(10))