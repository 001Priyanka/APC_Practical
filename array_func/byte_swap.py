from array import array

arr = array('i', [1, 2, 3])

print("Before byteswap:", arr)

arr.byteswap()

print("After byteswap:", arr)