# Q11. Create Student with roll_no, name, and course.
# Derive Result with marks in three subjects.
# Calculate total, percentage, and grade.

class Student:
    def __init__(self, roll_no, name, course):
        self.roll_no = roll_no
        self.name = name
        self.course = course


class Result(Student):
    def __init__(self, roll_no, name, course, marks):
        super().__init__(roll_no, name, course)
        self.marks = marks

    def total(self):
        return sum(self.marks)

    def percentage(self):
        return self.total() / 3

    def grade(self):
        p = self.percentage()

        if p >= 90:
            return "A+"
        elif p >= 80:
            return "A"
        elif p >= 70:
            return "B"
        elif p >= 60:
            return "C"
        else:
            return "D"

    def display(self):
        print("Name:", self.name)
        print("Roll No:", self.roll_no)
        print("Course:", self.course)
        print("Total:", self.total())
        print("Percentage:", self.percentage())
        print("Grade:", self.grade())


r = Result(101, "Pallavi", "MCA", [85, 90, 80])
r.display()