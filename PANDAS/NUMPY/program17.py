import numpy as np

marks = np.array([
    70, 85, 60, 90, 75,
    80, 65, 95, 88, 72,
    55, 78, 82, 68, 91,
    74, 89, 63, 96, 77
])

average = np.mean(marks)

print("Class Average:", average)

print("\nStudents scoring above average:")
print(marks[marks > average])