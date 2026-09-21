num=tuple(map(int,input("enter the tuple values:").split()))
res=[]
for n in num:
    idx=num.index(n)
    postion_rept=idx+1
    for i in range(postion_rept):
        res.append(n)
print(tuple(res))
