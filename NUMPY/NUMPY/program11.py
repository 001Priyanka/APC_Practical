import numpy as np

arr = np.arange(1, 21)

print("Array:")
print(arr)

print("\nFirst 5 elements:")
print(arr[:5])

print("\nLast 5 elements:")
print(arr[-5:])

print("\nAlternate elements:")
print(arr[::2])

print("\nReverse order:")
print(arr[::-1])