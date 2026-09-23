# Q9. Create Person.
# Derive Student and Faculty from Person.
# Create TeachingAssistant inheriting from both Student and Faculty.
# Demonstrate multiple and hierarchical inheritance.

class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def __init__(self, name, course):
        super().__init__(name)
        self.course = course


class Faculty(Person):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject


class TeachingAssistant(Student, Faculty):
    def __init__(self, name, course, subject):
        Person.__init__(self, name)
        self.course = course
        self.subject = subject

    def display(self):
        print("Name:", self.name)
        print("Course:", self.course)
        print("Teaching Subject:", self.subject)


ta = TeachingAssistant("Pallavi", "MCA", "Python")
ta.display()