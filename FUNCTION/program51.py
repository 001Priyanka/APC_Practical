# 51. Take a list of products with names, prices, and quantities,
#     use functions and lambda expressions to:
#     a) Calculate total value of each product.
#     b) Filter products costing more than ₹1,000.
#     c) Sort products according to total value.

products = [
    ("Laptop", 50000, 2),
    ("Mouse", 500, 3),
    ("Keyboard", 1500, 2),
    ("Monitor", 10000, 1)
]

# a) Calculate total value
def total_value(product):
    return product[1] * product[2]

values = list(
    map(lambda x: (x[0], total_value(x)), products)
)

# b) Filter products costing more than 1000
filtered = list(
    filter(lambda x: total_value(x) > 1000, products)
)

# c) Sort according to total value
sorted_products = sorted(
    products,
    key=lambda x: total_value(x)
)

print("Total value of products:")
print(values)

print("\nProducts costing more than 1000:")
print(filtered)

print("\nProducts sorted by total value:")
print(sorted_products)