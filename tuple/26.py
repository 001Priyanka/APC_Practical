tuple1 = (10, 20, 30, 40, 50)
tuple2 = (30, 40, 50, 60, 70)

common = ()

for n in tuple1:
    if n in tuple2:
        common += (n,)

print("Common elements:", common)