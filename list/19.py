students = ["Amit", "Priya", "Rahul", "Sneha"]

print("Total Students:", len(students))

name = input("Enter student name to search: ")

if name in students:
    print(name, "is present.")
else:
    print(name, "is absent.")

new_student = input("Enter new student name: ")
students.append(new_student)

absent = input("Enter absent student name to remove: ")

if absent in students:
    students.remove(absent)

print("Updated Student List:", students)