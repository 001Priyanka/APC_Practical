# 48. Take employee records containing name and salary,
#     sort them according to salary using lambda.

employees = [
    ("Amit", 45000),
    ("Rahul", 60000),
    ("Sneha", 50000),
    ("Priya", 75000)
]

employees.sort(key=lambda employee: employee[1])

print("Employees sorted by salary:")

for employee in employees:
    print(employee)