email = input("Enter email: ")

if "@" in email and "." in email:
    at = email.index("@")
    dot = email.rindex(".")

    if at > 0 and dot > at + 1 and dot < len(email)-1:
        print("Valid Email")
    else:
        print("Invalid Email")
else:
    print("Invalid Email")