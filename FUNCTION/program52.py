# 52. Write a program using functions, map(), filter(), and lambda expressions
#     to process a list of words and:
#     a) Find the length of every word.
#     b) Extract words having more than five characters.
#     c) Sort words according to their length.

words = input("Enter words: ").split()

# a) Find length of every word
lengths = list(map(lambda word: len(word), words))

# b) Words having more than five characters
long_words = list(filter(lambda word: len(word) > 5, words))

# c) Sort words according to length
sorted_words = sorted(words, key=lambda word: len(word))

print("Length of words =", lengths)
print("Words having more than five characters =", long_words)
print("Words sorted by length =", sorted_words)