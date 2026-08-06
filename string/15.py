string = input("Enter a string: ")

printed = ""

for ch in string:
    if string.count(ch) > 1 and ch not in printed:
        print(ch)
        printed += ch