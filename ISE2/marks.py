# student_marks.py

marks = (
    int(input("Enter marks for Subject 1: ")),
    int(input("Enter marks for Subject 2: ")),
    int(input("Enter marks for Subject 3: "))
)

print("Student Marks:", marks)

position = int(input("Enter the subject number (1-3): "))

if 1 <= position <= 3:
    print("Selected Subject Marks:", marks[position - 1])
else:
    print("Invalid subject number!")