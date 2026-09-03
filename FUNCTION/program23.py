# 23. Write a program using separate functions to process student records
#     containing name, roll number, and marks in five subjects.
#     Calculate total, percentage, grade, class average, highest scorer,
#     and lowest scorer.

def calculate_total(marks):
    return sum(marks)

def calculate_percentage(total):
    return total / 5

def calculate_grade(percentage):
    if percentage >= 90:
        return "A"
    elif percentage >= 75:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"

students = []

n = int(input("Enter number of students: "))

for i in range(n):
    name = input("Enter name: ")
    roll = input("Enter roll number: ")

    marks = []
    for j in range(5):
        marks.append(float(input("Enter marks: ")))

    total = calculate_total(marks)
    percentage = calculate_percentage(total)
    grade = calculate_grade(percentage)

    students.append({
        "name": name,
        "roll": roll,
        "total": total,
        "percentage": percentage,
        "grade": grade
    })

total_percentage = 0

for student in students:
    total_percentage += student["percentage"]

class_average = total_percentage / n

highest = max(students, key=lambda x: x["percentage"])
lowest = min(students, key=lambda x: x["percentage"])

for student in students:
    print("\nName:", student["name"])
    print("Roll:", student["roll"])
    print("Total:", student["total"])
    print("Percentage:", student["percentage"])
    print("Grade:", student["grade"])

print("\nClass Average =", class_average)
print("Highest Scorer =", highest["name"])
print("Lowest Scorer =", lowest["name"])