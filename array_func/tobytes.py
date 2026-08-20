from array import array

arr = array('i', [10, 20, 30])

data = arr.tobytes()

print("Array:", arr)
print("Bytes:", data)