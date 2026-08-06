sentence = input("Enter a sentence: ")

words = sentence.split()

result = ""

for word in words:
    result += word[0].upper() + word[1:] + " "

print("Title Case:", result)