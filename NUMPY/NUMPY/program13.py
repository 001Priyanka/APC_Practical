import numpy as np

arr = np.array([50, 10, 80, 30, 20, 90, 40])

print("Original Array:")
print(arr)

print("\nAscending order:")
print(np.sort(arr))

print("\nDescending order:")
print(np.sort(arr)[::-1])