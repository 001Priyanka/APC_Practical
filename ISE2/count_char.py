# count_characters.py

filename = input("Enter file name: ")

vowels = 0
consonants = 0
digits = 0
special = 0

try:
    with open(filename, "r") as file:
        text = file.read()

    for ch in text:
        if ch.isalpha():
            if ch.lower() in "aeiou":
                vowels += 1
            else:
                consonants += 1
        elif ch.isdigit():
            digits += 1
        elif not ch.isspace():
            special += 1

    print("Vowels:", vowels)
    print("Consonants:", consonants)
    print("Digits:", digits)
    print("Special characters:", special)

except FileNotFoundError:
    print("File not found!")