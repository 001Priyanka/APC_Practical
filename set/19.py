morning = {"Amit", "Rahul", "Priya", "Sneha"}
afternoon = {"Priya", "Sneha", "Rohan", "Kiran"}

both_sessions = morning.intersection(afternoon)
only_morning = morning - afternoon
only_afternoon = afternoon - morning
at_least_one = morning.union(afternoon)

print("Students present in both sessions:", both_sessions)
print("Students only in morning:", only_morning)
print("Students only in afternoon:", only_afternoon)
print("Students present in at least one session:", at_least_one)