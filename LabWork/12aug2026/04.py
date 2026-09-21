num=tuple(map(int,input("enter the tuple values:").split()))
res=[]
avg=sum(num)//len(num)
for n in num:
    if n>avg:
        res.append(n)
print(tuple(res))
