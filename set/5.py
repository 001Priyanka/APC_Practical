students = {"Rahul", "Priya", "Amit", "Sneha", "Rohan"}

name = input("Enter student name: ")

if name in students:
    print("Student exists in the set.")
else:
    print("Student does not exist in the set.")