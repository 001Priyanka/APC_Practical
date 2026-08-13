runs = (45, 78, 32, 100, 56, 89, 23, 67, 91, 50)

total = 0
highest = runs[0]
lowest = runs[0]

for score in runs:
    total += score

    if score > highest:
        highest = score

    if score < lowest:
        lowest = score

average = total / len(runs)

print("Total runs:", total)
print("Highest score:", highest)
print("Lowest score:", lowest)
print("Average score:", average)