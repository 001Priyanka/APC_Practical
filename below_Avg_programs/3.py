#Write a PYTHON program that reads the number 
# and check the no is positive or negative.

n = int(input("Enter a number: "))

if n<0:
    print("The number is -ve")
elif n>0:
    print("The number is +ve")
else:
    print("The number is 0.")
