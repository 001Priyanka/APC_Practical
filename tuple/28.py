numbers = (10, 20, 10, 30, 20, 10, 40, 30)

frequency = {}

for n in numbers:
    if n in frequency:
        frequency[n] += 1
    else:
        frequency[n] = 1

for n in frequency:
    print(n, "appears", frequency[n], "times")