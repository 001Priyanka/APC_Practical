cart = ["Milk", "Bread", "Butter"]

# Add item
cart.append("Eggs")

# Remove item
cart.remove("Bread")

# Search item
item = input("Enter item to search: ")

if item in cart:
    print(item, "is in the cart.")
else:
    print(item, "is not in the cart.")

# Display cart
print("Shopping Cart:", cart)

# Count items
print("Total Items:", len(cart))