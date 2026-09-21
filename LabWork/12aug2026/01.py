num=tuple(map(int,(input("Enter the tuple values :").split())))
res=[]
for n in num:
    idx=num.index(n)
    res.append(n)
    res.append(idx)
print(tuple(res))
