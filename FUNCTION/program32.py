# 32. Create separate functions for addition, subtraction,
#     multiplication, and division. Pass these functions as arguments
#     to another function called calculate().

def addition(a, b):
    return a + b

def subtraction(a, b):
    return a - b

def multiplication(a, b):
    return a * b

def division(a, b):
    return a / b

def calculate(a, b, operation):
    return operation(a, b)

print("Addition =", calculate(10, 5, addition))
print("Subtraction =", calculate(10, 5, subtraction))
print("Multiplication =", calculate(10, 5, multiplication))
print("Division =", calculate(10, 5, division))