# 20. Write a function that accepts basic salary and calculates gross salary
#     after adding HRA and DA.

def gross_salary(basic):
    hra = basic * 0.20
    da = basic * 0.10

    gross = basic + hra + da

    return gross

basic = float(input("Enter basic salary: "))

print("Gross Salary =", gross_salary(basic))