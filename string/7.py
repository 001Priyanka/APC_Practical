string = input("Enter a string: ")

result = ""

for ch in string:
    if ch != ' ':
        result += ch

print("String without spaces =", result)