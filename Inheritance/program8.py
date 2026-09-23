# Q8. Create Employee with employee ID, name, and basic salary.
# Create Manager, Developer, and Tester classes.
# Each calculates salary differently based on allowances.

class Employee:
    def __init__(self, emp_id, name, basic_salary):
        self.emp_id = emp_id
        self.name = name
        self.basic_salary = basic_salary


class Manager(Employee):
    def calculate_salary(self):
        return self.basic_salary + (self.basic_salary * 0.40)


class Developer(Employee):
    def calculate_salary(self):
        return self.basic_salary + (self.basic_salary * 0.30)


class Tester(Employee):
    def calculate_salary(self):
        return self.basic_salary + (self.basic_salary * 0.20)


m = Manager(101, "Pallavi", 50000)
d = Developer(102, "Rahul", 40000)
t = Tester(103, "Sneha", 35000)

print("Manager Salary:", m.calculate_salary())
print("Developer Salary:", d.calculate_salary())
print("Tester Salary:", t.calculate_salary())