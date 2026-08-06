string = input("Enter a string: ")

result = ""
count = 1

for i in range(len(string)-1):
    if string[i] == string[i+1]:
        count += 1
    else:
        result += string[i] + str(count)
        count = 1

result += string[-1] + str(count)

print("Encoded String:", result)