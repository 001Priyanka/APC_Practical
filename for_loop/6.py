import math

x = float(input("Enter the value of x in degrees: "))
n = int(input("Enter number of terms: "))

x = x * math.pi / 180

sum = 0

for i in range(n):
    power = 2 * i
    term = ((-1) ** i) * (x ** power) / math.factorial(power)
    sum = sum + term

print("cos(x) =", sum)