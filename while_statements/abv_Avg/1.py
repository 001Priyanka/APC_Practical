n = int(input("Enter a number: "))

if n <= 1:
    print("Not Prime")
else:
    flag = 0

    for i in range(2, n):
        if n % i == 0:
            flag = 1
            break

    if flag == 0:
        print("Prime Number")
    else:
        print("Not Prime Number")