from array import array

arr = array('i', [10, 20])

b = array('i', [30, 40]).tobytes()

arr.frombytes(b)

print(arr)