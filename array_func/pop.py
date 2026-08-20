from array import array

arr = array('i', [10, 20, 30, 40])

removed = arr.pop()

print("Removed element:", removed)
print("Array after pop:", arr)