paragraph = input("Enter paragraph: ")

words = paragraph.lower().split()

freq = {}

for word in words:
    freq[word] = freq.get(word, 0) + 1

for word in freq:
    print(word, ":", freq[word])