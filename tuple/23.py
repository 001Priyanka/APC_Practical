prices = (100, 250, 150, 500, 200)

total = 0
highest = prices[0]
lowest = prices[0]

for price in prices:
    total += price

    if price > highest:
        highest = price

    if price < lowest:
        lowest = price

average = total / len(prices)

print("Total bill:", total)
print("Average price:", average)
print("Highest price:", highest)
print("Lowest price:", lowest)