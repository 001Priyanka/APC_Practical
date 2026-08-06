string = input("Enter a string: ")

reverse = ""

for ch in string:
    reverse = ch + reverse

print("Reversed String =", reverse)