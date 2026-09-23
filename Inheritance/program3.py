# Q3. Create Academic and Sports classes.
# Academic stores marks and Sports stores sports points.
# Student inherits from both and calculates overall performance.

class Academic:
    def __init__(self, marks):
        self.marks = marks


class Sports:
    def __init__(self, sports_points):
        self.sports_points = sports_points


class Student(Academic, Sports):
    def __init__(self, name, marks, sports_points):
        Academic.__init__(self, marks)
        Sports.__init__(self, sports_points)
        self.name = name

    def performance(self):
        return self.marks + self.sports_points

    def display(self):
        print("Name:", self.name)
        print("Academic Marks:", self.marks)
        print("Sports Points:", self.sports_points)
        print("Overall Performance:", self.performance())


s = Student("Pallavi", 80, 15)
s.display()