import numpy as np

arr = np.arange(1, 28).reshape(3, 3, 3)

flat = arr.flatten()

print("3D Array:")
print(arr)

print("\nFlattened Array:")
print(flat)

print("\nSum:", np.sum(flat))
print("Average:", np.mean(flat))
print("Maximum:", np.max(flat))
print("Minimum:", np.min(flat))