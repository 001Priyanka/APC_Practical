# 50. Take employee records containing name, department, and salary,
#     use filter(), map(), and sorted() with lambda functions to:
#     a) Find employees earning more than ₹50,000.
#     b) Increase salaries by 10%.
#     c) Sort employees according to salary.

employees = [
    ("Amit", "IT", 60000),
    ("Rahul", "HR", 45000),
    ("Sneha", "IT", 70000),
    ("Priya", "Sales", 50000)
]

# a) Employees earning more than 50000
high_salary = list(filter(lambda x: x[2] > 50000, employees))

# b) Increase salary by 10%
increased_salary = list(
    map(lambda x: (x[0], x[1], x[2] * 1.10), employees)
)

# c) Sort according to salary
sorted_employees = sorted(employees, key=lambda x: x[2])

print("Employees earning more than 50000:")
print(high_salary)

print("\nSalaries after 10% increase:")
print(increased_salary)

print("\nEmployees sorted by salary:")
print(sorted_employees)