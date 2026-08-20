from array import array

arr1 = array('i', [10, 20, 30])

data = arr1.tobytes()

print("Original array:", arr1)
print("Converted to bytes:", data)

arr2 = array('i')
arr2.frombytes(data)

print("Converted back to array:", arr2)