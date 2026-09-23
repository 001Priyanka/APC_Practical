from array import array

arr = array('i', [10, 20, 30, 40])

with open("data.bin", "wb") as file:
    arr.tofile(file)

print("Array written to file.")