sales = list(map(int, input("Enter the values: ").split()))
streak = []
longest = []
for i in range(len(sales)):
    if i == 0 or sales[i] > sales[i - 1]:
        streak.append(sales[i])
    else:
        streak = [sales[i]]

    if len(streak) > len(longest):
        longest = streak.copy()

print("Longest increasing streak:", longest)
print("Number of days:", len(longest))
