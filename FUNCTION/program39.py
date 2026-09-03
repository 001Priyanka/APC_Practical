# 39. Use map() with lambda to calculate the cube of every element in a list.

numbers = list(map(int, input("Enter numbers: ").split()))

cubes = list(map(lambda x: x ** 3, numbers))

print("Cubes =", cubes)