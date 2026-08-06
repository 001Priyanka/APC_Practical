string = input("Enter the main string: ")
sub = input("Enter substring: ")

if sub in string:
    print("Substring found")
else:
    print("Substring not found")