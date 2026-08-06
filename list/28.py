scores = []

print("Enter scores of 10 matches:")

for i in range(10):
    scores.append(int(input()))

highest = scores[0]
lowest = scores[0]
total = 0

century = 0
half = 0

for score in scores:
    total += score

    if score > highest:
        highest = score

    if score < lowest:
        lowest = score

    if score >= 100:
        century += 1
    elif score >= 50:
        half += 1

average = total / len(scores)

print("Highest Score:", highest)
print("Lowest Score:", lowest)
print("Total Runs:", total)
print("Average Runs:", average)
print("Centuries:", century)
print("Half-centuries:", half)