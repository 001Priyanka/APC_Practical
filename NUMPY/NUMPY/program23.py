import numpy as np

arr = np.arange(1, 25).reshape(2, 3, 4)

print("Original 3D Array:")
print(arr)

flat = arr.flatten()

print("\nFlattened Array:")
print(flat)