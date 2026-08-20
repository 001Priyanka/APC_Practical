sentence = input("Enter a sentence: ")

words = sentence.split()

unique_words = set(words)

print("Unique words:")

for word in unique_words:
    print(word)