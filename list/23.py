numbers = [10, 20, 10, 30, 20, 10, 40]

visited = []

for num in numbers:
    if num not in visited:
        count = 0
        for i in numbers:
            if i == num:
                count += 1
        print(num, "occurs", count, "times")
        visited.append(num)