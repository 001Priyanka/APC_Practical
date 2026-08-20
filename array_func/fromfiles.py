from array import array

arr = array('i', [10, 20, 30, 40])

with open("numbers.bin", "wb") as file:
    arr.tofile(file)

new_arr = array('i')

with open("numbers.bin", "rb") as file:
    new_arr.fromfile(file, 4)

print("Array read from file:", new_arr)