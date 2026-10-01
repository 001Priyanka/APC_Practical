import numpy as np

arr = np.arange(1, 25).reshape(2, 3, 4)

print("Array:")
print(arr)

print("\nSum of all elements:")
print(np.sum(arr))

print("\nSum of each layer:")
print(np.sum(arr, axis=(1, 2)))

print("\nSum along rows:")
print(np.sum(arr, axis=2))

print("\nSum along columns:")
print(np.sum(arr, axis=1))