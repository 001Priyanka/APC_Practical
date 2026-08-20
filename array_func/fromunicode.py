from array import array

arr = array('u')

arr.fromunicode("Hello")

print("Array:", arr)
print("As string:", arr.tounicode())