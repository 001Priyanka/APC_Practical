# 46. Take a list of words; sort them according to their length using lambda.

words = input("Enter words: ").split()

words.sort(key=lambda word: len(word))

print("Sorted words =", words)