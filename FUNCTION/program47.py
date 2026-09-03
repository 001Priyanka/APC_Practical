# 47. Take a list of tuples containing student names and marks,
#     sort the students according to their marks using lambda.

students = [
    ("Amit", 75),
    ("Pallavi", 90),
    ("Rahul", 65),
    ("Sneha", 85)
]

students.sort(key=lambda student: student[1])

print("Students sorted by marks:")

for student in students:
    print(student)