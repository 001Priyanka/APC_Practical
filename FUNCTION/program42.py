# 42. Take a list of integers, use filter() with an appropriate
#     lambda expression to identify prime numbers.

def is_prime(n):
    if n < 2:
        return False

    for i in range(2, n):
        if n % i == 0:
            return False

    return True

numbers = list(map(int, input("Enter numbers: ").split()))

prime_numbers = list(filter(lambda x: is_prime(x), numbers))

print("Prime numbers =", prime_numbers)