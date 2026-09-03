# 21. Create a function that accepts item prices and quantities
#     and returns the total bill after applying a discount.

def total_bill(prices, quantities):
    total = 0

    for i in range(len(prices)):
        total += prices[i] * quantities[i]

    if total >= 5000:
        discount = total * 0.20
    elif total >= 2000:
        discount = total * 0.10
    else:
        discount = 0

    return total - discount

prices = list(map(float, input("Enter prices: ").split()))
quantities = list(map(int, input("Enter quantities: ").split()))

print("Final Bill =", total_bill(prices, quantities))