import numpy as np

a = np.array([
    [1, 2],
    [3, 4]
])

b = np.array([
    [5, 6],
    [7, 8]
])

print("Array A:")
print(a)

print("\nArray B:")
print(b)

print("\nHorizontal Concatenation:")
print(np.hstack((a, b)))

print("\nVertical Concatenation:")
print(np.vstack((a, b)))