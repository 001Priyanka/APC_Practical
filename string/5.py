string = input("Enter a string: ")

upper = lower = 0

for ch in string:
    if 'A' <= ch <= 'Z':
        upper += 1
    elif 'a' <= ch <= 'z':
        lower += 1

print("Uppercase letters =", upper)
print("Lowercase letters =", lower)