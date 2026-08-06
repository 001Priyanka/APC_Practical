salary = []

n = int(input("Enter number of employees: "))

for i in range(n):
    salary.append(int(input("Enter salary: ")))

highest = salary[0]
lowest = salary[0]
total = 0

above50 = 0
below30 = 0

for s in salary:
    total += s

    if s > highest:
        highest = s

    if s < lowest:
        lowest = s

    if s > 50000:
        above50 += 1

    if s < 30000:
        below30 += 1

average = total / len(salary)

print("Highest Salary:", highest)
print("Lowest Salary:", lowest)
print("Average Salary:", average)
print("Employees earning above ₹50,000:", above50)
print("Employees earning below ₹30,000:", below30)