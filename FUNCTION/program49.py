# 49. Take a list containing student names and marks,
#     use functions and lambda expressions to:
#     a) Calculate average marks.
#     b) Filter students scoring above 75.
#     c) Sort students according to marks.

students = [
    ("Amit", 70),
    ("Pallavi", 90),
    ("Rahul", 60),
    ("Sneha", 85)
]

def average_marks(students):
    total = sum(map(lambda x: x[1], students))
    return total / len(students)

average = average_marks(students)

above_75 = list(filter(lambda x: x[1] > 75, students))

sorted_students = sorted(students, key=lambda x: x[1])

print("Average Marks =", average)
print("Students above 75 =", above_75)
print("Sorted Students =", sorted_students)