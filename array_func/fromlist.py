from array import array

arr = array('i')

numbers = [10, 20, 30, 40]

arr.fromlist(numbers)

print("Array after fromlist:", arr)