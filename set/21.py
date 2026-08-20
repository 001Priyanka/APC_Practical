python_students = {"Amit", "Rahul", "Priya", "Sneha"}
java_students = {"Priya", "Sneha", "Rohan", "Kiran"}

both_courses = python_students.intersection(java_students)
only_one_course = python_students.symmetric_difference(java_students)

print("Students enrolled in both courses:", both_courses)
print("Students enrolled in only one course:", only_one_course)