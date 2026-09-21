num=tuple(map(int,input("enter the tuple values:").split()))
res=[]
for n in num:
    bkp=n
    s=0
    while n>0:
        d=n%10
        s=s+d
        n=n//10
    res.append(bkp)
    res.append(s)
print(tuple(res))
