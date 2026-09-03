# 7. Write a function that accepts n and returns the sum of the first n natural numbers.

def sum_natural(n):
    total = 0

    for i in range(1, n + 1):
        total += i

    return total

n = int(input("Enter n: "))
print("Sum =", sum_natural(n))