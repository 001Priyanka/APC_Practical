# 27. Create functions to calculate consultation charges,
#     laboratory charges, medicine charges, room charges,
#     and final bill. Apply discounts based on patient category.

def consultation_charge():
    return 500

def laboratory_charge():
    return 1000

def medicine_charge():
    return 1500

def room_charge(days):
    return days * 1000

def final_bill(category, days):
    total = (consultation_charge() +
             laboratory_charge() +
             medicine_charge() +
             room_charge(days))

    if category.lower() == "senior":
        discount = total * 0.20
    elif category.lower() == "child":
        discount = total * 0.10
    else:
        discount = 0

    return total - discount

category = input("Enter patient category: ")
days = int(input("Enter room days: "))

print("Final Bill =", final_bill(category, days))