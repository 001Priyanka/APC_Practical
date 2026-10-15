# main.py

import arithmetic

a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

print("Addition:", arithmetic.add(a, b))
print("Subtraction:", arithmetic.subtract(a, b))
print("Multiplication:", arithmetic.multiply(a, b))
print("Division:", arithmetic.divide(a, b))