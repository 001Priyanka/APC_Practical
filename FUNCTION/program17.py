# 17. Write a function that accepts n and returns the first n Fibonacci numbers.

def fibonacci(n):
    result = []
    a = 0
    b = 1

    for i in range(n):
        result.append(a)
        a, b = b, a + b

    return result

n = int(input("Enter n: "))

print("Fibonacci =", fibonacci(n))