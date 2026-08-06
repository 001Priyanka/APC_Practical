sentence = input("Enter a sentence: ")

count = 0
in_word = False

for ch in sentence:
    if ch != ' ' and not in_word:
        count += 1
        in_word = True
    elif ch == ' ':
        in_word = False

print("Total words =", count)