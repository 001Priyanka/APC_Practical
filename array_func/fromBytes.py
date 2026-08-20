from array import array

arr = array('i', [10, 20, 30])

data = array('i', [40, 50]).tobytes()

arr.frombytes(data)

print("Array after frombytes:", arr)