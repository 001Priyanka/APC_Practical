password = input("Enter password: ")

upper = lower = digit = special = 0

for ch in password:
    if 'A' <= ch <= 'Z':
        upper += 1
    elif 'a' <= ch <= 'z':
        lower += 1
    elif '0' <= ch <= '9':
        digit += 1
    else:
        special += 1

if len(password) >= 8 and upper >= 1 and lower >= 1 and digit >= 1 and special >= 1:
    print("Valid Password")
else:
    print("Invalid Password")