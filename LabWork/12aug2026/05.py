num=tuple(map(int,input("enter the tuple values:").split()))
res=[]
for n in num:
    idx=num.index(n)
    if idx%2==0:
        res.append(n**2)
    else:
        res.append(n**3)
print(tuple(res))
