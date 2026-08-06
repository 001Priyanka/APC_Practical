string = input("Enter a string: ")

vowels = consonants = digits = spaces = special = 0

for ch in string:
    if ch in "aeiouAEIOU":
        vowels += 1
    elif ('a' <= ch <= 'z') or ('A' <= ch <= 'Z'):
        consonants += 1
    elif '0' <= ch <= '9':
        digits += 1
    elif ch == ' ':
        spaces += 1
    else:
        special += 1

print("Vowels =", vowels)
print("Consonants =", consonants)
print("Digits =", digits)
print("Spaces =", spaces)
print("Special Characters =", special)