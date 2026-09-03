# 18. Create a function that accepts marks in five subjects and returns
#     the student's percentage and grade.

def percentage_grade(marks):
    total = sum(marks)
    percentage = total / 5

    if percentage >= 90:
        grade = "A"
    elif percentage >= 75:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:
        grade = "F"

    return percentage, grade

marks = []

for i in range(5):
    marks.append(float(input("Enter marks: ")))

percentage, grade = percentage_grade(marks)

print("Percentage =", percentage)
print("Grade =", grade)