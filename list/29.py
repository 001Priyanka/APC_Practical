temperature = []

print("Enter temperature of 30 days:")

for i in range(30):
    temperature.append(float(input()))

highest = temperature[0]
lowest = temperature[0]
total = 0

for temp in temperature:
    total += temp

    if temp > highest:
        highest = temp

    if temp < lowest:
        lowest = temp

average = total / len(temperature)

above = 0
below = 0

for temp in temperature:
    if temp > average:
        above += 1
    elif temp < average:
        below += 1

print("Hottest Day Temperature:", highest)
print("Coldest Day Temperature:", lowest)
print("Average Temperature:", average)
print("Days Above Average:", above)
print("Days Below Average:", below)