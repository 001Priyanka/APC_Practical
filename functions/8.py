def power(base, exponent):
    result = 1

    for i in range(exponent):
        result *= base

    return result

print(power(2, 5))