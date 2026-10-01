import numpy as np

arr = np.array([10, 25, 55, 60, 35, 80, 45, 90, 20, 70])

print("Original Array:")
print(arr)

arr[arr > 50] = 0

print("\nAfter replacement:")
print(arr)