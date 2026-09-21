x = list(map(lambda row: list(map(int, row.split())), input().split(",")))
h=0
l=[]
for n in x:
    Sum=sum(n)
    if Sum>h:
        h=Sum
        l=n
print(l)

