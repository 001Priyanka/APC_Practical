# Write a PYTHON program to find smallest of three numbers

a = int(input("Enter first number: "))
b = int(input("Enter second number: "))
c = int(input("Enter third number: "))

if a <= b and a <= c:
    print(a, "is the smallest number")
elif b <= a and b <= c:
    print(b, "is the smallest number")
else:
    print(c, "is the smallest number")