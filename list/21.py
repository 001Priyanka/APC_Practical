list1 = []
list2 = []

print("Enter 5 elements for List 1:")

for i in range(5):
    list1.append(int(input()))

print("Enter 5 elements for List 2:")

for i in range(5):
    list2.append(int(input()))

merged = list1 + list2

print("Merged List:", merged)