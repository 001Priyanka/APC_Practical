numbers = [10, 20, 30, 40, 50]

# Left rotation
left = numbers[1:] + [numbers[0]]
print("Left Rotation :", left)

# Right rotation
right = [numbers[-1]] + numbers[:-1]
print("Right Rotation:", right)