# 26. Develop a modular program using functions to calculate electricity bills
#     using different consumption slabs. Include fixed charges, taxes, and discounts.

def calculate_units_charge(units):
    if units <= 100:
        return units * 5
    elif units <= 200:
        return 100 * 5 + (units - 100) * 7
    else:
        return 100 * 5 + 100 * 7 + (units - 200) * 10

def calculate_tax(amount):
    return amount * 0.05

def calculate_discount(amount):
    if amount > 5000:
        return amount * 0.10
    return 0

def electricity_bill(units):
    fixed_charge = 100

    unit_charge = calculate_units_charge(units)
    subtotal = unit_charge + fixed_charge

    tax = calculate_tax(subtotal)
    discount = calculate_discount(subtotal)

    final_bill = subtotal + tax - discount

    return final_bill

units = int(input("Enter units: "))

print("Final Electricity Bill =", electricity_bill(units))