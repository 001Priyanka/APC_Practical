# 28. Implement functions to add/remove products, calculate subtotal,
#     apply coupon discounts, calculate GST, and generate the final invoice.

products = {}

def add_product(name, price, quantity):
    products[name] = {
        "price": price,
        "quantity": quantity
    }

def remove_product(name):
    if name in products:
        del products[name]

def subtotal():
    total = 0

    for product in products.values():
        total += product["price"] * product["quantity"]

    return total

def coupon_discount(amount, coupon):
    if coupon == "SAVE10":
        return amount * 0.10
    return 0

def calculate_gst(amount):
    return amount * 0.18

def invoice(coupon):
    sub = subtotal()
    discount = coupon_discount(sub, coupon)

    amount_after_discount = sub - discount
    gst = calculate_gst(amount_after_discount)

    final = amount_after_discount + gst

    print("Subtotal =", sub)
    print("Discount =", discount)
    print("GST =", gst)
    print("Final Amount =", final)

add_product("Laptop", 50000, 1)
add_product("Mouse", 1000, 2)

invoice("SAVE10")