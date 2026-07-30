import math

n = int(input("Enter a number: "))

root = int(math.sqrt(n))

if root * root != n:
    print("The number does not have an integer square root")

elif root < 2:
    print("Square root is not prime")

else:
    prime = True

    for i in range(2, root):
        if root % i == 0:
            prime = False
            break

    if prime:
        print("Square root is prime")
    else:
        print("Square root is not prime")