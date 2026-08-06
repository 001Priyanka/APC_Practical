string = input("Enter a string: ")

checked = ""

for ch in string:
    if ch not in checked:
        print(ch, "=", string.count(ch))
        checked += ch