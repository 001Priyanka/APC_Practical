temperatures = (32, 35, 31, 30, 34, 36, 33)

total = 0
maximum = temperatures[0]
minimum = temperatures[0]

for temp in temperatures:
    total += temp

    if temp > maximum:
        maximum = temp

    if temp < minimum:
        minimum = temp

average = total / len(temperatures)

print("Maximum temperature:", maximum)
print("Minimum temperature:", minimum)
print("Average temperature:", average)