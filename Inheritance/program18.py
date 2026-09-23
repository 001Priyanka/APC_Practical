# Q18. Create Person and derive Doctor and Patient.
# Create Surgeon and MedicalResearcher.
# Demonstrate multiple inheritance and hierarchical inheritance.

class Person:
    def __init__(self, name):
        self.name = name


class Doctor(Person):
    def treat(self):
        print(self.name, "is treating patients.")


class Patient(Person):
    def checkup(self):
        print(self.name, "is going for a checkup.")


class Surgeon(Doctor):
    def surgery(self):
        print(self.name, "performs surgery.")


class MedicalResearcher(Doctor):
    def research(self):
        print(self.name, "does medical research.")


class ResearchSurgeon(Surgeon, MedicalResearcher):
    def special_work(self):
        print(self.name, "performs surgery and medical research.")


doctor = Surgeon("Dr. Patil")
researcher = MedicalResearcher("Dr. Sharma")
rs = ResearchSurgeon("Dr. Mehta")

doctor.treat()
doctor.surgery()

researcher.treat()
researcher.research()

rs.treat()
rs.surgery()
rs.research()
rs.special_work()