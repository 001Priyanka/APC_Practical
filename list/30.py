names = ["Amit", "Priya", "Rahul"]
ages = [25, 30, 40]

# Add patient
name = input("Enter patient name: ")
age = int(input("Enter patient age: "))

names.append(name)
ages.append(age)

# Delete patient
delete = input("Enter patient name to delete: ")

if delete in names:
    index = names.index(delete)
    names.pop(index)
    ages.pop(index)

# Search patient
search = input("Enter patient name to search: ")

if search in names:
    index = names.index(search)
    print("Patient Found")
    print("Name:", names[index])
    print("Age:", ages[index])
else:
    print("Patient Not Found")

# Display all patients
print("\nPatient Details:")

for i in range(len(names)):
    print(names[i], "-", ages[i], "years")

print("Total Patients:", len(names))