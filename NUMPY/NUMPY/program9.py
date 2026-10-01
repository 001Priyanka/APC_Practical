import numpy as np

arr = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
])

print("Matrix:")
print(arr)

print("\nFirst Row:")
print(arr[0])

print("\nLast Column:")
print(arr[:, -1])

print("\nDiagonal Elements:")
print(np.diag(arr))

print("\nSecond and Third Rows:")
print(arr[1:3])