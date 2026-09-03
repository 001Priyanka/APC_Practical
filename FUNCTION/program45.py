# 45. Take a list of words, use filter() and lambda
#     to find words having more than five characters.

words = input("Enter words: ").split()

result = list(filter(lambda word: len(word) > 5, words))

print("Words =", result)