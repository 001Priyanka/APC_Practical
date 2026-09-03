# 10. Define a function that accepts a string and returns the number of vowels present in it.

def count_vowels(text):
    count = 0

    for ch in text:
        if ch.lower() in "aeiou":
            count += 1

    return count

text = input("Enter a string: ")
print("Number of vowels =", count_vowels(text))