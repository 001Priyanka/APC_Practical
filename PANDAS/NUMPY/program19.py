import numpy as np

arr = np.arange(1, 25).reshape(2, 3, 4)

print("Array:")
print(arr)

print("\nFirst Element:")
print(arr[0, 0, 0])

print("\nLast Element:")
print(arr[-1, -1, -1])

print("\nElement at [0,1,2]:")
print(arr[0, 1, 2])

print("\nElement at [1,2,3]:")
print(arr[1, 2, 3])