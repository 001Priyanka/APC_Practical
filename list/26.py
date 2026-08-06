marks = []

print("Enter marks of 20 students:")

for i in range(20):
    marks.append(int(input()))

highest = marks[0]
lowest = marks[0]
total = 0

for m in marks:
    total += m

    if m > highest:
        highest = m

    if m < lowest:
        lowest = m

average = total / len(marks)

above = 0
below = 0

for m in marks:
    if m > average:
        above += 1
    elif m < average:
        below += 1

print("Highest Marks:", highest)
print("Lowest Marks:", lowest)
print("Average Marks:", average)
print("Students Above Average:", above)
print("Students Below Average:", below)