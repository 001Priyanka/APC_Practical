numbers = (10, 20, 30, 40)

numbers = list(numbers)

numbers[1] = 25
numbers.append(50)

numbers = tuple(numbers)

print("Modified tuple:", numbers)