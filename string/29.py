sentence = input("Enter sentence: ")

words = sentence.split()

for i in range(len(words)-1, -1, -1):
    print(words[i], end=" ")