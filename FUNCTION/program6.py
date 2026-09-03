# 6. Define a function to calculate the area of a circle using its radius.

def area_circle(r):
    return 3.14 * r * r

r = float(input("Enter radius: "))
print("Area of circle =", area_circle(r))